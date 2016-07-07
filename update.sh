#!/bin/bash

VERSION="$1"

if [[ -z "${VERSION}" ]]; then
    echo "Please pass the new version first."
    exit 1
fi

sed ciao.spec.in -e "s/\#\#VERSION\#\#/${VERSION}/g" > ciao.spec
make generateupstream && make || exit 1

git add ciao.spec Makefile release upstream testresults
git commit -s -m "Update to ${VERSION}"
make bump
