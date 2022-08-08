var gulp = require('gulp');
var sass = require('gulp-sass');
var rename = require('gulp-rename');
var uglify = require('gulp-uglify');
var cleanCSS = require('gulp-clean-css');
// var react = require('gulp-react');

gulp.task('default', function () {
  return gulp.src('./searchs/static/*.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSS())
    .pipe(rename("css.css"))
    .pipe(gulp.dest('./searchs/static'));
});

gulp.task('javascript', function(){
    return gulp.src('./searchs/static/jsdev.js')
        .pipe(uglify())
        .pipe(rename('js.js'))
        .pipe(gulp.dest('./searchs/static'));

});
// gulp.task('react', function(){
//     return gulp.src('./searchs/static/*.jsx')
//         .pipe(react())
//         .pipe(gulp.dest('./searchs/static'));
// });

gulp.task('watch', function () {
  gulp.watch('./searchs/static/*.scss', ['default']);
  gulp.watch('./searchs/static/jsdev.js', ['javascript']);
});