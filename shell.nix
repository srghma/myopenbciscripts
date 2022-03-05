# https://nixos.wiki/wiki/Python
# https://github.com/nix-community/pypi2nix
# https://github.com/nix-community/poetry2nix

{ pkgs ? import /home/srghma/projects/nixpkgs {} }:

let
pypi2nix = import (pkgs.fetchgit {
  url = "https://github.com/nix-community/pypi2nix";
  # adjust rev and sha256 to desired version
  rev = "v2.0.4";
  sha256 = "sha256:0mxh3x8bck3axdfi9vh9mz1m3zvmzqkcgy6gxp8f9hhs6qg5146y";
}) { inherit pkgs; };
in

# :l /home/srghma/projects/nixpkgs
# :l <nixpkgs>
# :l <nixos>
# :b pkgs.python37Packages.pygame
# :b pkgs.python38Packages.pygame
# :b pkgs.python39Packages.pygame
# :b pkgs.python310Packages.pygame
# :b pkgs.python311Packages.pygame

pkgs.mkShell {
  buildInputs = with pkgs; [
    (python39.withPackages (
      ps: with ps; [
        pygame
        python-osc
        numpy
        pydub
        pyaudio
      ]
    ))
    poetry
    # pypi2nix
  ];
}

# (pkgs.poetry2nix.mkPoetryEnv {
#   projectDir = ./.;
#   overrides = pkgs.poetry2nix.defaultPoetryOverrides.extend ( self: super: {
#     pygame = pkgs.python3Packages.pygame;
#   });
# })

# pkgs.poetry2nix.mkPoetryEnv {
#   projectDir = ./.;
# }

# let
#   python-with-my-packages = pkgs.python3.withPackages (p: with p; [
#     pygame
#     python-osc
#   ]);
# in
# python-with-my-packages.env
