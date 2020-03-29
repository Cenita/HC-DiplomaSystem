var gulp = require("gulp")
var cssnano = require("gulp-cssnano")
var rename = require("gulp-rename")
var uglify = require("gulp-uglify")
var concat = require("gulp-concat")
var imagemin = require("gulp-imagemin")
var cache = require("gulp-cache")
var  bs = require('browser-sync').create()
var sass = require('gulp-sass')
var path = {
    'html':'./html/',
    'css': './css/',
    'js':'./js/',
    'images':'./images/',
    'css_dist':'./dist/css/',
    'js_dist':'./dist/js/',
    'images_dist':'./dist/images/'
}

gulp.task("html",function () {
    gulp.src(path.html+'*.html')
        .pipe(bs.stream())
})

// 定义一个css的任务
gulp.task("css",function () {
    gulp.src(path.css+'*.scss')
        .pipe(sass().on("error",sass.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.css_dist))
        .pipe(bs.stream())
})

gulp.task("js",function () {
    gulp.src(path.js+'*.js')
        .pipe(uglify())
        .pipe(rename({"suffix":".min"}))
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream())
})

gulp.task("images",function () {
    gulp.src(path.images+'*.*')
        .pipe(cache(imagemin()))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream())
})



gulp.task("watch",function () {
    gulp.watch(path.css + '*.html',gulp.parallel("html"))
    gulp.watch(path.css + '*.scss',gulp.parallel("css"))
    gulp.watch(path.js + '*.js',gulp.parallel("js"))
    gulp.watch(path.images + '*.*',gulp.parallel("images"))
})

gulp.task("bs",function () {
    bs.init(
        {
            'server':{
                'baseDir':'./'
            }
        }
    )
})


gulp.task('default', gulp.series('bs','watch'));
