echo "Usage: bash.sh [-u] git_url [-p] port. You should execute this script within the project directory."

while getopts ":u:p:" opt; do
  case ${opt} in
    u )
      url=${OPTARG}
      ;;
    p )
      port=${OPTARG}
      ;;
    \? )
      exit 1
      ;;
  esac
done
mkdir "localserver"
cd ./localserver
git clone $url .
npm install
PORT=$port npm start &
echo "sleeping for 5 seconds to give enough time for the webserver to start before crawling"
sleep 5
cd ../
python main.py url http://localhost:$port