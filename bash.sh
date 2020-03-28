while getopts ":u:p:" opt; do
  case ${opt} in
    u )
      url=${OPTARG}
      ;;
    p )
      port=${OPTARG}
      ;;
    \? ) echo "Usage: cmd [-u] git url [-p] port"
      ;;
  esac
done
mkdir "localserver"
cd ./localserver
git clone $url .
npm install
PORT=$port npm start &
echo $port