export ZSH="/home/michael/.oh-my-zsh"

#ZSH_THEME="agnoster"
autoload -U colors && colors
PS1="%B%{$fg[red]%}[%{$fg[yellow]%}%n%{$fg[green]%}@%{$fg[blue]%}%M %{$fg[magenta]%}%~%{$fg[red]%}]%{$reset_color%}$%b "


[ -f "$HOME/.config/shortcutrc" ] && source "$HOME/.config/shortcutrc"
[ -f "$HOME/.config/aliasrc" ] && source "$HOME/.config/aliasrc"
echo -ne '\e[5 q'

preexec() { echo -ne '\e[5 q' ;}
# Command auto-correction.
ENABLE_CORRECTION="true"

# Command execution time stamp shown in the history command output.
HIST_STAMPS="mm/dd/yyyy"

# Plugins to load
plugins=(git
         sudo
	 zsh-autosuggestions
         zsh-syntax-highlighting)

autoload -U compinit && compinit
source $ZSH/oh-my-zsh.sh

autoload -U +X bashcompinit && bashcompinit
complete -o nospace -C /usr/bin/vault vault


# Bind home and end keys
bindkey '\e[1~' beginning-of-line
bindkey '\e[4~' end-of-line

# Fixes strange cursor position / formating bug

# Alias to open with corresponding default program
alias open=xdg-open
fetch=$(fetch)
logo="\e[H\e[2J
          \e[1;36m.
         \e[1;36m/#\\      \e[1;37m          _      \e[1;36m _ _
        \e[1;36m/###\\     \e[1;37m         | |     \e[1;36m| (_)
       \e[1;36m/p^###\\    \e[1;37m _ __ ___| |__   \e[1;36m| |_ _ __  _   ___  __
      \e[1;36m/##P^q##\\   \e[1;37m| '__/ __| '_ \\  \e[1;36m| | | '_ \\| | | \\ \\/ /
     \e[1;36m/##(   )##\\  \e[1;37m| | | (__| | | | \e[1;36m| | | | | | |_| |>  <
    \e[1;36m/###P   q#,^\\ \e[1;37m|_|  \\___|_| |_| \e[1;36m|_|_|_| |_|\\__,_/_/\\_\\ \e[0;37mTM
   \e[1;36m/P^         ^q\\"

echo ${logo}
echo ${fetch}
echo "\e[0m================================================================================"
echo "                           Welcome \e[34m$USER\e[0m"
echo ""
alias gogit='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
alias vim='nvim'
alias svim='sudo nvim'
