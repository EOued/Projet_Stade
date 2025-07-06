# PKGBUILD for teams manager


_realname="Teams Manager"
pkgbase=mingw-w64-${_realname}
pkgname="${MINGW_PACKAGE_PREFIX}-${_realname}"
pkgver=1.0
pkgrel=1
pkgdesc="Description: TODO"
arch=('any')
mingw_arch=('mingw64' 'ucrt64' 'clang64' 'clagarm64')

msys2_repository_url='https://gitlab.gnome.org/World/gedit/gedit/'
msys2_references=(
  "cpe: cpe:/a:gnome:gedit"
)
license=('spdx:GPL-2.0-or-later')
depends=("${MINGW_PACKAGE_PREFIX}-cairo"
         "${MINGW_PACKAGE_PREFIX}-gdk-pixbuf2"
         "${MINGW_PACKAGE_PREFIX}-gettext-runtime"
         "${MINGW_PACKAGE_PREFIX}-glib2"
         "${MINGW_PACKAGE_PREFIX}-gobject-introspection-runtime"
         "${MINGW_PACKAGE_PREFIX}-gsettings-desktop-schemas"
         "${MINGW_PACKAGE_PREFIX}-gspell"
         "${MINGW_PACKAGE_PREFIX}-gtk3"
         "${MINGW_PACKAGE_PREFIX}-libgedit-amtk"
         "${MINGW_PACKAGE_PREFIX}-libgedit-gfls"
         "${MINGW_PACKAGE_PREFIX}-libgedit-gtksourceview"
         "${MINGW_PACKAGE_PREFIX}-libgedit-tepl"
         "${MINGW_PACKAGE_PREFIX}-libpeas"
         "${MINGW_PACKAGE_PREFIX}-pango"
         "${MINGW_PACKAGE_PREFIX}-python-gobject"
         "${MINGW_PACKAGE_PREFIX}-adwaita-icon-theme")
makedepends=("${MINGW_PACKAGE_PREFIX}-cc"
             "${MINGW_PACKAGE_PREFIX}-meson"
             "${MINGW_PACKAGE_PREFIX}-pkgconf"
             "${MINGW_PACKAGE_PREFIX}-appstream-glib"
             "${MINGW_PACKAGE_PREFIX}-gobject-introspection"
             "${MINGW_PACKAGE_PREFIX}-gtk-doc"
             "${MINGW_PACKAGE_PREFIX}-gettext-tools"
             "${MINGW_PACKAGE_PREFIX}-itstool"
             "${MINGW_PACKAGE_PREFIX}-python"
             "${MINGW_PACKAGE_PREFIX}-yelp-tools"
             "${MINGW_PACKAGE_PREFIX}-desktop-file-utils"
             "git")
optdepends=("${MINGW_PACKAGE_PREFIX}-gedit-plugins: Additional features")
