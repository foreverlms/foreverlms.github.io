require "html-proofer"
task :default do
	puts "Running CI tasks..."

	sh("JEKYLL_ENV=production bundle exec jekyll build")
	# options = { :assume_extension => true }
 #  	HTMLProofer.check_directory("./_site", options).run
	puts "Jekyll successfully built"
end