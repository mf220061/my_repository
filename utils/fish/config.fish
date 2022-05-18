set -x VIRTUAL_ENV_DISABLE_PROMPT 1
set -g fish_prompt_pwd_dir_length 0

if test (service docker status | awk '{print $4}') = "not";
  sudo service docker start > /dev/null
end
