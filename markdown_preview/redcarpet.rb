#!/usr/bin/env ruby

require 'redcarpet'
require 'pygments'

html_tmpl = "<!DOCTYPE html>
<html>
	<head>
		<meta charset=\"utf-8\">
		<link href=\"/home/liberize/markdown/styles/markdown.css\" rel=\"stylesheet\">
		<link href=\"/home/liberize/markdown/styles/pygments.css\" rel=\"stylesheet\">
	</head>
	<body>
		{{ content }}
	</body>
</html>
"

# create a custom renderer
class MyHTML < Redcarpet::Render::HTML
	# highlight code with pygments
	def block_code(code, language)
		Pygments.highlight(code, :lexer => language)
		# uncomment the following line to add linenos to codeblocks
		# ('linenos' can be set to 'table' or 'inline')
		# Pygments.highlight(code, :lexer => language, :options => {:linenos => 'table'})
	end
end

# create markdown object with extensions
markdown = Redcarpet::Markdown.new(MyHTML, :fenced_code_blocks => true,
	:no_intra_emphasis => true, :autolink => true, :strikethrough => true,
	:superscript => true, :with_toc_data => true, :tables => true)

markdown_path = ARGV[0]
html_path = "#{markdown_path[/.*(?=\.[^\.]+$)/]}.html"

# read from markdown file
file = File.open(markdown_path, "r")
contents = file.read
file.close

# remove yaml front-matter
front_matter = contents.match(/^---\n(\w+:[^\n]*\n)+---\n/m)
if front_matter
	match = contents.match(/(?:^---\n(\w+:[^\n]*\n)*title:\s*")([^\n]*)(?="\s*\n(\w+:[^\n]*\n)*---\n)/m)
	title = match ? "# #{match[2]}\n" : "\n"
	contents[0, front_matter[0].length] = title
end

# convert content and write to html file
contents = markdown.render(contents)
html_tmpl["{{ content }}"] = contents
file = File.open(html_path, "w")
file.write(html_tmpl)
file.close

# open html in browser
system "xdg-open \"#{html_path}\" &"
