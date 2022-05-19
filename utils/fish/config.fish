set -x VIRTUAL_ENV_DISABLE_PROMPT 1
set -g fish_prompt_pwd_dir_length 0

if test (echo (service docker status | awk '{print $4}') | sed 's/  *//g') = "not";
  sudo service docker start > /dev/null
end
