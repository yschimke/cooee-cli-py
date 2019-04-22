function __fish_complete_cooee_command
	cooee --fish-complete (commandline -ct)
end

complete -c cooee -x -d 'Cooee CLI' -a '(__fish_complete_cooee_command)'
complete -c cooee -s h -l help -d 'Help options'
complete -c cooee -l login -d 'Login and link account'
complete -c cooee -l logout -d 'Unlink account'
complete -c cooee -l version -d 'Output version and exit'
complete -c cooee -l debug -d 'Enable debugging output'
complete -c cooee -l repl -d 'REPL'

complete -c cooee -l command-complete -d 'Complete possible bash command'
complete -c cooee -l fish-complete -d 'Complete possible fish command'
