#!/bin/bash
update_data() {
  git config --global user.email "maciv@hotmail.gr"
  git config --global user.name "Isabelle Viktoria Maciohsek"
  git checkout master
  git pull
  git add .
  git commit -m "Update - $(date +%Y.%m.%d_%H:%M)" --allow-empty
  git push --quiet "https://${GH_TOKEN}@github.com/Trinityyi/COVID-19-tools.git" master > /dev/null 2>&1
}

update_data
