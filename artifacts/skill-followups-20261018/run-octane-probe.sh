#!/bin/sh
# One isolated container, real installed framework, expected red mutation controls.
set -eu
cd /var/www/html
php -v | head -n 1
php -r '$lock=json_decode(file_get_contents("composer.lock"),true); foreach($lock["packages"] as $p){if(in_array($p["name"],["laravel/framework","laravel/octane"])) {echo $p["name"]," ",$p["version"],PHP_EOL;}}'
php -r 'foreach(["vendor/laravel/framework/src/Illuminate/Container/Container.php","vendor/laravel/framework/src/Illuminate/Foundation/Testing/TestCase.php","vendor/laravel/octane/src/Listeners/FlushTemporaryContainerInstances.php","vendor/laravel/octane/src/Worker.php"] as $p){echo hash_file("sha256",$p)," ",$p,PHP_EOL;}'
php -l /evidence/octane-probe.php
php -l /evidence/octane-snippet.php
php /evidence/octane-probe.php scoped
for mutant in singleton no-reset; do
    result=0
    php /evidence/octane-probe.php "$mutant" || result=$?
    test "$result" -eq 1
done
# Demonstrates the old rebuild mechanism's false green; not a full PHPUnit boot.
php /evidence/octane-probe.php rebuild-singleton
php /evidence/octane-probe.php scoped
printf '%s\n' 'PASS: corrected oracle green, both mutants red, restored green; rebuilt singleton falsely green.'
