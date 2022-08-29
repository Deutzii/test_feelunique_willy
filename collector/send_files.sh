# Name of the bucket (add /food or /cosmetic if multiple industry)
readonly DIR_NAME=feelunique_uk

# Setting the path of the targeted folders
s3_path_products="s3://voysen-data-collecte-bucket/$DIR_NAME/products/$(date +%Y)/$(date +%m)"
s3_path_reviews="s3://voysen-data-collecte-bucket/$DIR_NAME/reviews/$(date +%Y)/$(date +%m)"
s3_path_urls_aggregated="s3://voysen-data-collecte-bucket/$DIR_NAME/urls/urls_aggregated/$(date +%Y)/$(date +%m)"
s3_path_urls_to_collect="s3://voysen-data-collecte-bucket/$DIR_NAME/urls/urls_to_collect/$(date +%Y)/$(date +%m)"

# Find the most recent files which will be uploaded on S3
merged_products=$(find /home/ec2-user/ec2-collector/merged_products -type f -name "*.json")
merged_reviews=$(find /home/ec2-user/ec2-collector/merged_reviews -type f -name "*.json")

if [ "$1" == 0 ]; then
  true
else
  urls_aggregated=$(find /home/ec2-user/ec2-collector/urls_aggregated -type f -name "*.json")
  urls_to_collect=$(find /home/ec2-user/ec2-collector/urls_to_collect_anchor -type f -name "*.json")
fi

# Display some information
echo "--------------------------------------------------"
echo "-----       SENDING FILES TO S3 BUCKET       -----"
echo "--------------------------------------------------"
echo "> TARGETED BUCKET                 | $DIR_NAME"
echo "> NUMBER OF MERGED PRODUCTS FILE  | $(wc -w <<<"$merged_products")"
echo "> NUMBER OF MERGED REVIEWS FILE   | $(wc -w <<<"$merged_reviews")"
echo "> NUMBER OF URLS AGGREGATED FILE  | $(wc -w <<<"$urls_aggregated")"
echo "> NUMBER OF URLS TO COLLECT FILES | $(wc -w <<<"$urls_to_collect")"
echo "--------------------------------------------------"

# Start of the upload
function upload() {
  echo ">>> UPLOAD STARTED <<<"

  # Merged products
  # There can be multiple files to upload, so we use a loop to do it one by one
  for file in $merged_products; do
    # We replace the potentially wrong collect date by the current one
    new_merged_products="$(date +%Y_%m_01)_${file#*_*_*_*_}"
    # Upload of the urls to collect file with a timestamp at the end
    aws s3 cp "$file" "$s3_path_products/${new_merged_products}"
    echo -e "\n"
  done

  # Merged reviews
  # We replace the potentially wrong collect date by the current one
  # There can be multiple files to upload, so we use a loop to do it one by one
  for file in $merged_reviews; do
    # We replace the potentially wrong collect date by the current one
    new_merged_reviews="$(date +%Y_%m_01)_${file#*_*_*_*_}"
    # Upload of the urls to collect file with a timestamp at the end
    aws s3 cp "$file" "$s3_path_reviews/${new_merged_reviews}"
    echo -e "\n"
  done

  # Aggregated urls
  # There can be multiple files to upload, so we use a loop to do it one by one
  for file in $urls_aggregated; do
    # We replace the potentially wrong collect date by the current one
    new_urls_aggregated="$(date +%Y_%m_01)_${file#*_*_*_*_}"
    # Upload of the urls to collect file with a timestamp at the end
    aws s3 cp "$file" "$s3_path_urls_aggregated/${new_urls_aggregated%.*}_$(date +%m_%d).${new_urls_aggregated##*.}"
    echo -e "\n"
  done

  # Urls to collect
  # There can be multiple files to upload, so we use a loop to do it one by one
  for file in $urls_to_collect; do
    # We replace the potentially wrong collect date by the current one
    new_urls_to_collect="$(date +%Y_%m_01)_${file#*_*_*_*_*_*_}"
    # Upload of the urls to collect file with a timestamp at the end
    aws s3 cp "$file" "$s3_path_urls_to_collect/${new_urls_to_collect%.*}_$(date +%m_%d).${new_urls_to_collect##*.}"
    echo -e "\n"
  done
  echo ">>> UPLOAD COMPLETED <<<"

  exit
}

# Asking confirmation
echo "DO YOU WISH TO START THE UPLOAD?"
select yn in "START" "CANCEL"; do
  case $yn in
  "START")
    upload
    ;;
  "CANCEL")
    echo ">>> UPLOAD CANCELLED <<<"
    exit
    ;;
  *) echo "($REPLY) IS NOT A VALID OPTION. PLEASE, SELECT A VALID OPTION." ;;
  esac
done
echo "--------------------------------------------------"
