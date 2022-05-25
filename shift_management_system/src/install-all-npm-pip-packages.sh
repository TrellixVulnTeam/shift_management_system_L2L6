#!/bin/sh
dryrun=false
help=false
npm=false
pip=false

while getopts d:v-: opt; do
    # OPTARG を = の位置で分割して opt と optarg に代入
    optarg="$OPTARG"
    [[ "$opt" = - ]] &&
        opt="-${OPTARG%%=*}" &&
        optarg="${OPTARG/${OPTARG%%=*}/}" &&
        optarg="${optarg#=}"

    case "-$opt" in
        --dryrun)
            dryrun=true
            ;;
        --npm)
            npm=true
            ;;
        --pip)
            pip=true
            ;;
        --help)
            help=true
            ;;
        --|-\?|--*)
            echo "$0: illegal option -- ${opt##-}" >&2
            exit 1
            ;;
    esac
done

function my_echo () {
  echo -e "\033[1;32m${1}\033[0;39m"
}

if $help; then
  echo "このスクリプトでは、カレントディレクトリからnpmやpipのinstallスクリプトを検索し、順次実行していきます。"
  echo "[引数の説明]"
  echo "--npm : npm-install.sh の検索・実行を行います。"
  echo "--pip : pip-install.sh の検索・実行を行います。"
  echo "--dryrun : スクリプトの検索だけを行います。実行は行いません。"
  exit
fi

if [ $npm = true -a $pip = true ]; then
  echo "--npm オプションと --pip オプションは併用出来ません。どちらか一つを指定して下さい。"
  exit 1
fi

script_name="npm-install.sh"
if $pip; then
  script_name="pip-install.sh"
fi

pwd=`pwd`
find ./ -type f -name $script_name -not -path "*node-modules*" -not -path "*site-packages*" -not -path "*cdk.out*" | while read -r fname
do
  fname=$(echo $fname | sed -e "s/^\.//")
  fullpath=$pwd$fname
  dirname=$(echo $fullpath | sed -e "s/${script_name}//")
  my_echo "${dirname}${script_name}"
  cd $dirname
  my_echo "exec ${script_name}"
  if $dryrun; then
    echo ''
  else
    ./${script_name}
  fi
  my_echo "done!!"
  cd $pwd
  echo ''
done
