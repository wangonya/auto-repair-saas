#!/bin/sh -l

set -e

[ -z "${INPUT_GITHUB_TOKEN}" ] && {
	echo 'Missing input "github_token: ${{ secrets.GITHUB_TOKEN }}".'
	exit 1
}

docs_src=$GITHUB_WORKSPACE/docs
docs_html=$GITHUB_WORKSPACE/gh-pages
sphinx_doctree=$GITHUB_WORKSPACE/.doctree

echo ::group::Create working directories
echo "mkdir $docs_src"
mkdir -p $docs_src
echo "mkdir $docs_html"
mkdir -p $docs_html
echo "mkdir $sphinx_doctree"
mkdir -p $sphinx_doctree
echo ::endgroup::

# checkout branch docs
echo ::group::Initializing the repository
echo "cd $docs_src"
cd $docs_src
echo "git init"
git init
echo "git remote add origin https://github.com/$GITHUB_REPOSITORY.git"
git remote add origin https://$GITHUB_ACTOR:$INPUT_GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git
echo ::endgroup::
echo ::group::Fetching the repository
echo "git fetch origin +$GITHUB_SHA:refs/remotes/origin/docs"
git fetch origin +$GITHUB_SHA:refs/remotes/origin/docs
echo ::endgroup::
echo ::group::Checkout ref
echo "git checkout -B docs refs/remotes/origin/docs"
git checkout -B docs refs/remotes/origin/docs
echo ::endgroup::
echo ::group::Show HEAD message
git log -1
echo ::endgroup::

# get author
author_name="$(git show --format=%an -s)"
author_email="$(git show --format=%ae -s)"
docs_sha8="$(echo ${GITHUB_SHA} | cut -c 1-8)"

# outputs
echo "::set-output name=name::"$author_name""
echo "::set-output name=email::"$author_email""
echo "::set-output name=docs_sha::$(echo ${GITHUB_SHA})"
echo "::set-output name=docs_sha8::"$docs_sha8""

# checkout branch gh-pages
echo ::group::Initializing branch gh-pages
echo "cd $docs_html"
cd $docs_html
echo "git init"
git init
echo "git remote add origin https://github.com/$GITHUB_REPOSITORY.git"
git remote add origin https://$GITHUB_ACTOR:$INPUT_GITHUB_TOKEN@github.com/$GITHUB_REPOSITORY.git
echo ::endgroup::

# check remote branch exist first
echo ::group::Check remote branch gh-pages exist
echo "git ls-remote --heads origin refs/heads/gh-pages"
gh_pages_exist=$(git ls-remote --heads origin refs/heads/gh-pages)
if [ -z "$gh_pages_exist" ]; then
	echo "Not exist."
else
	echo "Exist"
fi
echo ::endgroup::

if [ -z "$gh_pages_exist" ]; then
	echo ::group::Create branch gh-pages
	echo "git checkout -B gh-pages"
	git checkout -B gh-pages
	echo ::endgroup::
else
	echo ::group::Fetching branch gh-pages
	echo "git fetch origin +refs/heads/gh-pages:refs/remotes/origin/gh-pages"
	git fetch origin +refs/heads/gh-pages:refs/remotes/origin/gh-pages
	echo "git checkout -B gh-pages refs/remotes/origin/gh-pages"
	git checkout -B gh-pages refs/remotes/origin/gh-pages
	echo "git log -1"
	git log -1
	echo ::endgroup::
fi

# git config
echo ::group::Set commiter
echo "git config user.name $author_name"
git config user.name $author_name
echo "git config user.email $author_email"
git config user.email $author_email
echo ::endgroup::

# sphinx extensions
if [ "$INPUT_INSTALL_EXTENSIONS" = true ]; then
	echo ::group::Installing sphinx extensions
	echo "pip3 install -r $docs_src/$INPUT_SOURCE_DIR/requirements.txt"
	pip3 install django
	echo ::endgroup::
fi

# sphinx-build
echo ::group::Sphinx build html
echo "sphinx-build -b html $docs_src/$INPUT_SOURCE_DIR $docs_html -E -d $sphinx_doctree"
sphinx-build -b html $docs_src/$INPUT_SOURCE_DIR $docs_html -E -d $sphinx_doctree
echo ::endgroup::

# auto creation of README.md
if [ "$INPUT_CREATE_README" = true ]; then
	echo ::group::Create README
	echo "Create file README.md with these content"
	echo "GitHub Pages of [$GITHUB_REPOSITORY](https://github.com/$GITHUB_REPOSITORY.git)" >README.md
	echo "===" >>README.md
	echo "Sphinx html documentation of [$docs_sha8](https://github.com/$GITHUB_REPOSITORY/tree/$GITHUB_SHA)" >>README.md
	cat README.md
	echo ::endgroup::
fi

# commit and push
echo ::group::Push
echo "git add ."
git add .
echo 'git commit --allow-empty -m "From $GITHUB_REF $docs_sha8"'
git commit --allow-empty -m "From $GITHUB_REF $docs_sha8"
echo "git push origin gh-pages"
git push origin gh-pages
echo ::endgroup::
