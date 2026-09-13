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
  ];

  postVenvCreation = ''
    unset SOURCE_DATE_EPOCH
    pip install -e . --no-build-isolation
  '';
  postShellHook = ''
    unset SOURCE_DATE_EPOCH
  '';
}