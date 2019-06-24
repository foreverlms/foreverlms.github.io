task :default do
	puts "Running CI tasks..."

	sh("JEKYLL_ENV=production bundle exec jekyll build")
	sh("JEKYLL_ENV=production bundle exec htmlproofer ./_site --allow-hash-href --check-html --disable-external")
	puts "Jekyll successfully built"
end