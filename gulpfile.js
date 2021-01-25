// gulpfile.js
let gulp = require('gulp');
let sass = require('gulp-sass'),
  postcss = require('gulp-postcss'),
  autoprefixer = require('autoprefixer'),
  cssnano = require('cssnano'),
  sourcemaps = require('gulp-sourcemaps');

let browserSync = require('browser-sync').create();

// Put this after including our dependencies
let paths = {
  styles: {
    // By using styles/**/*.sass we're telling gulp to check all folders for any sass file
    src: './static/scss/*.scss',
    // Compiled files will end up in whichever folder it's found in (partials are not compiled)
    dest: './static/css/',
  },

  // Easily add additional paths
  // ,html: {
  //  src: '...',
  //  dest: '...'
  // }
};

// Define tasks after requiring dependencies
function style() {
  return (
    gulp
      .src(paths.styles.src)
      // Initialize sourcemaps before compilation starts
      .pipe(sourcemaps.init())
      .pipe(sass())
      .on('error', sass.logError)
      // Use postcss with autoprefixer and compress the compiled file using cssnano
      .pipe(postcss([autoprefixer(), cssnano()]))
      // Now add/write the sourcemaps
      .pipe(sourcemaps.write())
      .pipe(gulp.dest(paths.styles.dest))
      // Add browsersync stream pipe after compilation
      .pipe(browserSync.stream())
  );
}

function watch() {
  browserSync.init({
    // You can tell browserSync to use this directory and serve it as a mini-server
    server: {
      baseDir: './',
    },
    // If you are already serving your website locally using something like apache
    // You can use the proxy setting to proxy that instead
    // proxy: "yourlocal.dev"
  });
  // gulp.watch takes in the location of the files to watch for changes
  // and the name of the function we want to run on change
  style();
  gulp.watch(paths.styles.src, style);
  // We should tell gulp which files to watch to trigger the reload
  // This can be html or whatever you're using to develop your website
  // Note -- you can obviously add the path to the Paths object
  //gulp.watch('path/to/html/*.html', reload);
}

// Don't forget to expose the task!
exports.watch = watch;

// Expose the task by exporting it
// This allows you to run it from the commandline using
// $ gulp style
exports.style = style;
