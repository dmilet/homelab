# Lines configured by zsh-newuser-install
HISTFILE=~/.histfile
HISTSIZE=1000
SAVEHIST=1000
bindkey -v
# End of lines configured by zsh-newuser-install
# The following lines were added by compinstall
zstyle :compinstall filename '/home/david/.zshrc'

autoload -Uz compinit
compinit
# End of lines added by compinstall
#
export PATH=/home/david/.local/bin:$PATH

eval ssh-agent
ssh-add /home/david/.ssh/id_ed25519

alias kubectl="microk8s kubectl"

# Added by Toolbox App
export PATH="$PATH:/home/david/.local/share/JetBrains/Toolbox/scripts"
