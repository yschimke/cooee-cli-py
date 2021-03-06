#@IgnoreInspection BashAddShebang

function _cooee_debug ()
{
  echo "$*" >> /tmp/cooeecomplete.log
  return
}

function _cooee_is_cache_valid ()
{
  local cache_file line pos cache_line cache_pos
  cache_file=$1
  pos=$2
  line=$3

  _cooee_debug "checking $pos $line"
  if [[ -f "$cache_file" ]]; then
    cache_pos=$(sed '1q;d' ${cache_file})
    cache_line=$(sed '2q;d' ${cache_file})

    _cooee_debug "cache has $cache_pos $cache_line"

    if [[ "$line" = "$cache_line" ]] && [[ "$pos" = "$cache_pos" ]]; then
      _cooee_debug "match"
      return 0
    else
      _cooee_debug "no match"
      return 1
    fi
  else
    _cooee_debug "no file"

    return 1
  fi
}

_cooee_complete()
{
  local cur prev words cword cachefile line
  COMPREPLY=()
	job="${COMP_WORDS[0]}"
	cur="${COMP_WORDS[COMP_CWORD]}"
	prev="${COMP_WORDS[COMP_CWORD-1]}"
	line=${COMP_LINE/#cooee }

	_get_comp_words_by_ref -n : cur

  if [[ ${cur} == -* ]]; then
      _cooee_options="-h --help --version -l --local --command-complete --fish-complete --debug --login --logout"
      COMPREPLY=( $( compgen -W "$_cooee_options" -- "$cur" ) )
      return;
  fi

  cache_file="${TMPDIR}cooee-complete.cache"

  _cooee_debug $cache_file

  if _cooee_is_cache_valid ${cache_file} ${COMP_POINT} "$line"; then
    _cooee_commands=$(tail -n +3 ${cache_file})
  else
    _cooee_debug "running"
    _cooee_commands=$(cooee --command-complete "$line")
    echo "$COMP_POINT" > $cache_file
    echo "$line" >> $cache_file
    echo "$_cooee_commands" >> $cache_file
    _cooee_debug "ran"
  fi

  COMPREPLY=( $( compgen -W "$_cooee_commands" -- "$cur" ) )

  __ltrim_colon_completions "$cur"
}

complete -F _cooee_complete cooee
