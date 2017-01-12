#!/bin/bash

VERSION=`curl https://api.github.com/repos/01org/ciao/tags\?per_page=1 | awk -F '"' '/name/ {print $4}'`

if [[ -z "${VERSION}" ]]; then
    echo "Please pass the new version first."
    exit 1
fi

# get old version/release for commit message
OLDREL=$(cat release)
OLDVER=$(grep 'Version  : ' ciao.spec | sed -e "s/Version\ \ :\ //g")

# get the release number from the `release` file and increment +1
NEWREL=$(cat release | sed 's/$/+1/g' | bc)
sed ciao.spec.in \
    -e "s/\#\#RELEASE\#\#/${NEWREL}/g" \
    -e "s/\#\#VERSION\#\#/${VERSION}/g" > ciao.spec
echo ${NEWREL} > release
make generateupstream && make || exit 1

git add ciao.spec Makefile release upstream testresults
git commit -s -m "Update from version ${OLDVER}-${OLDREL} to version ${VERSION}-${NEWREL}"
