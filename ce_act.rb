class YourScript < Formula
    include Language::Python::Virtualenv

    desc "Arista CE ACT CLI tool"
    homepage "https://github.com/wdion-arista/ce_act_cli"
    url "https://github.com/wdion-arista/ce_act_cli/archive/v1.0.0.tar.gz"
    sha256 "abc123..." # Replace with the actual SHA256 of your tarball

    depends_on "python@3.12.9"

    def install
        virtualenv_install_with_resources
    end

    test do
        system bin/"ce_act", "--version"
    end
end
