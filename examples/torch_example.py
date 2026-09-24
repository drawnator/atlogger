import sys
import logging
from functools import cache
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from tqdm.auto import tqdm

from atlogger import ATLOGGER, WandbHandler, log

config = dict(
    epochs=10,
    classes=10,
    kernels=[16, 32],
    batch_size=128,
    learning_rate=0.005,
    dataset="MNIST",
    architecture="CNN")

@cache
def get_device():
  return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

@log("model")
def model_pipeline(config):
  model, train_loader, test_loader, criterion, optimizer = make(config)
  print(model)

  train(model, train_loader, criterion, optimizer, config)

  test_accuracy(model, test_loader)

  return model

def make(config):
    train, test = get_data(train=True), get_data(train=False)
    train_loader = make_loader(train, batch_size=config["batch_size"])
    test_loader = make_loader(test, batch_size=config["batch_size"])

    model = ConvNet(config["kernels"], config["classes"]).to(get_device())

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        model.parameters(), lr=config["learning_rate"])
    
    return model, train_loader, test_loader, criterion, optimizer

def get_data(slice=5, train=True):
    full_dataset = torchvision.datasets.MNIST(root=".",
                                              train=train, 
                                              transform=transforms.ToTensor(),
                                              download=True)
    sub_dataset = torch.utils.data.Subset(
      full_dataset, indices=range(0, len(full_dataset), slice))
    
    return sub_dataset


def make_loader(dataset, batch_size):
    loader = torch.utils.data.DataLoader(dataset=dataset,
                                         batch_size=batch_size, 
                                         shuffle=True,
                                         pin_memory=True, num_workers=2)
    return loader

class ConvNet(nn.Module):
    def __init__(self, kernels, classes=10):
        super(ConvNet, self).__init__()
        
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, kernels[0], kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, kernels[1], kernel_size=5, stride=1, padding=2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2))
        self.fc = nn.Linear(7 * 7 * kernels[-1], classes)

    @log()    
    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = out.reshape(out.size(0), -1)
        out = self.fc(out)
        return out

def train(model, loader, criterion, optimizer, config):
    wandbhandlr.run.watch(model, criterion, log="all", log_freq=10)

    total_batches = len(loader) * config["epochs"]
    example_ct = 0  # number of examples seen
    batch_ct = 0
    for epoch in tqdm(range(config["epochs"])):
        for _, (images, labels) in enumerate(loader):
            loss = train_batch(images, labels, model, optimizer, criterion)
            example_ct +=  len(images)
            batch_ct += 1
            if ((batch_ct + 1) % 25) == 0:
                train_log(loss, example_ct, epoch)


@log("loss")
def train_batch(images, labels, model, optimizer, criterion):
    images, labels = images.to(get_device()), labels.to(get_device())
    outputs = model(images)
    loss = criterion(outputs, labels)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return loss

# @log("loss")
def train_log(loss, example_ct, epoch):
  # run.log({"epoch": epoch, "loss": loss}, step=example_ct)
  print(f"Loss after {str(example_ct).zfill(5)} examples: {loss:.3f}")
  return {"epoch": epoch, "loss": loss}

@log()
def test_accuracy(model, test_loader):
    model.eval()
    with torch.no_grad():
        correct, total = 0, 0
        for images, labels in test_loader:
            images, labels = images.to(get_device()), labels.to(get_device())
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        accuracy = correct / total
        print(f"Accuracy of the model on the {total} " +
            f"test images: {accuracy:%}")
    return accuracy

if __name__ == "__main__":
  global wandbhandlr
  wandbhandlr = WandbHandler(
    project="pytorch-demo",
    config={"config":config},
    level="DEBUG"
  )
  streamhadlr = logging.StreamHandler()
  streamhadlr.setLevel(logging.WARN)
  ATLOGGER.addHandler(streamhadlr)
  ATLOGGER.addHandler(wandbhandlr)
  model_pipeline(config)