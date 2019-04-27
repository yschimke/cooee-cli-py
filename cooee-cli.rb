class CooeeCli < Formula
  desc "Coo.ee CLI"
  homepage "https://github.com/yschimke/cooee-cli-py"
  version "0.1"
  url "file:///Users/yuri/workspace/cooee-cli-py/buck-out/gen/cooee-cli__/cooee-cli.zip"
#   sha256 "97c304c18a89fcbe59e2d0f8d6767f777ec811529713ca8796c93c41b6cb566d"
#   head "https://github.com/yschimke/cooee-cli.git"

  depends_on :java
  depends_on "buck"

  def install
    bin.install "buck-out/gen/cooee/cooee.pex" => "cooee"
    bash_completion.install "shell/completion.bash" => "cooee"
    fish_completion.install "shell/cooee.fish"
  end
end
