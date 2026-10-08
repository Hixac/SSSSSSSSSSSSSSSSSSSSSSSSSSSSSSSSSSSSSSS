{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  packages = with pkgs; [
    nodejs
  ];

  languages = {
    typescript = {
      enable = true;
    };

    python = {
      enable = true;

      venv.enable = true;
      lsp.enable = false;

      directory = "server/";

      uv = {
        enable = true;
        sync.enable = true;
      };
    };
  };

  # https://devenv.sh/services/
  # services.postgres.enable = true;
}
