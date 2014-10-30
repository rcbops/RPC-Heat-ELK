# Heat Templates Template Site

This is a basic jekyll site that allows anyone to put some information about 
RPC's heat templates into specific places and immediately have a brand new 
templates site.

## Requirements

[jekyll](http://jekyllrb.com/) which requires ruby and rubygems to be 
installed. If you can do `gem install jekyll` you should be fine.

## Usage

To see the site, run `jekyll serve`. If you run this immediately after cloning 
and visit `http://localhost:4000/` in your browser, you should see sections 
that tell you where to put content.

1. Use Ctrl-C to kill the server

1. Open the `_config.yml` file to edit it:

  - Change the line that starts with `template_name: `

  - Change the URLs for `project_url` and `releases_url`

  - Optionally, change the `release` number

1. Run `jekyll serve` again

1. Edit the markdown files in `_includes/`.

1. Refresh the page to see the changes appear

1. Remove this file
