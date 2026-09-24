{ pkgs ? import <nixpkgs> {} }:

let
  python = pkgs.python313;
in
pkgs.mkShell rec {
  name = "atlogger-dev";

  venvDir = "./.venv";
  buildInputs = [
    python
    python.pkgs.venvShellHook
    python.pkgs.pip
    python.pkgs.setuptools
    python.pkgs.wandb
    #examples
    python.pkgs.torch
    python.pkgs.torchvision
    python.pkgs.numpy
    python.pkgs.keras
    python.pkgs.tensorflow
    python.pkgs.tqdm
    python.pkgs.jupyter
    python.pkgs.notebook
  ];

  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -e . --no-build-isolation
  '';
  postShellHook = ''
    unset SOURCE_DATE_EPOCH
  '';
}