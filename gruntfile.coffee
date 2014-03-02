module.exports = (grunt)->
  'use strict'

  GRUNT_CHANGED_PATH = '.grunt-changed-file'
  if grunt.file.exists GRUNT_CHANGED_PATH
    changed = grunt.file.read GRUNT_CHANGED_PATH
    grunt.file.delete GRUNT_CHANGED_PATH
    changed_only = (file)-> file is changed
  else
    changed_only = -> true

  data = {}

  grunt.initConfig
    watch:
      jade:
        files: 'public/**/*.jade'
        tasks: 'jade'
      stylus:
        files: 'public/**/*.styl'
        tasks: 'stylus'
      coffee:
        files: 'public/**/*.coffee'
        tasks: 'coffee'
      options:
        livereload: true
    jade:
      files:
        expand : true
        src    : 'public/**/*.jade'
        options: data: data
        ext    : '.html'
        # filter : changed_only
    stylus:
      files:
        expand : true
        src    : 'public/**/*.styl'
        ext    : '.css'
        # filter : changed_only
    coffee:
      files:
        expand : true
        src    : 'public/**/*.coffee'
        ext    : '.js'
        # filter : changed_only

  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-jade'
  grunt.loadNpmTasks 'grunt-contrib-stylus'
  grunt.loadNpmTasks 'grunt-contrib-coffee'

  grunt.registerTask 'default', ['watch']
  grunt.registerTask 'build'  , ['jade', 'stylus', 'coffee']
