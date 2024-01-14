import io
import re
from typing import BinaryIO, Optional
import textwrap

from repo_autoindex import autoindex
from repo_autoindex._impl.base import GeneratedIndex

REPOMD_XML = textwrap.dedent(
    """
    <?xml version="1.0" encoding="UTF-8"?>
    <repomd xmlns="http://linux.duke.edu/metadata/repo" xmlns:rpm="http://linux.duke.edu/metadata/rpm">
    <revision>1657165688</revision>
    <data type="primary">
        <checksum type="sha256">d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf</checksum>
        <open-checksum type="sha256">6fc4eddd4e9de89246efba3815b8a9dec9dfe168e4fd3104cc792dff908a0f62</open-checksum>
        <location href="repodata/d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf-primary.xml.gz"/>
        <timestamp>1657165688</timestamp>
        <size>2932</size>
        <open-size>16585</open-size>
    </data>
    <data type="filelists">
        <checksum type="sha256">284769ec79daa9e0a3b0129bb6260cc6271c90c4fe02b43dfa7cdf7635fb803f</checksum>
        <open-checksum type="sha256">72f89223c8b0f6c7a2ee6ed7fbd16ee0bb395ca68260038bb3895265af84c29f</open-checksum>
        <location href="repodata/284769ec79daa9e0a3b0129bb6260cc6271c90c4fe02b43dfa7cdf7635fb803f-filelists.xml.gz"/>
        <timestamp>1657165688</timestamp>
        <size>4621</size>
        <open-size>36911</open-size>
    </data>
    <data type="other">
        <checksum type="sha256">36c2195bbee0c39ee080969abc6fd59d943c3471114cfd43c6e776ac20d7ed21</checksum>
        <open-checksum type="sha256">39f52cf295db14e863abcd7b2eede8e6c5e39ac9b2f194349459d29cd492c90f</open-checksum>
        <location href="repodata/36c2195bbee0c39ee080969abc6fd59d943c3471114cfd43c6e776ac20d7ed21-other.xml.gz"/>
        <timestamp>1657165688</timestamp>
        <size>1408</size>
        <open-size>8432</open-size>
    </data>
    <data type="primary_db">
        <checksum type="sha256">55e6bfd00e889c5c1f9a3c9fb35a660158bc5d975ae082d434f3cf81cc2c0c21</checksum>
        <open-checksum type="sha256">b2692c49d1d98d68e764e29108d8a81a3dfd9e04fa7665115853a029396d118d</open-checksum>
        <location href="repodata/55e6bfd00e889c5c1f9a3c9fb35a660158bc5d975ae082d434f3cf81cc2c0c21-primary.sqlite.bz2"/>
        <timestamp>1657165688</timestamp>
        <size>7609</size>
        <open-size>114688</open-size>
        <database_version>10</database_version>
    </data>
    <data type="filelists_db">
        <checksum type="sha256">de63a509812c37f7736fcef0b79e9c55dfe67a2d77006f74fdc442935103e9e6</checksum>
        <open-checksum type="sha256">40eb5d53fe547c98d470813256c9bfc8a239b13697d8eb824a1485c9e186a0e3</open-checksum>
        <location href="repodata/de63a509812c37f7736fcef0b79e9c55dfe67a2d77006f74fdc442935103e9e6-filelists.sqlite.bz2"/>
        <timestamp>1657165688</timestamp>
        <size>10323</size>
        <open-size>65536</open-size>
        <database_version>10</database_version>
    </data>
    <data type="other_db">
        <checksum type="sha256">9aa39b62df200cb3784dea24092d0c1c686afff0cd0990c2ec7a61afe8896e1c</checksum>
        <open-checksum type="sha256">3e5cefb10ce805b827e12ca3b4839bba873dc9403fd92b60a364bf6f312bd972</open-checksum>
        <location href="repodata/9aa39b62df200cb3784dea24092d0c1c686afff0cd0990c2ec7a61afe8896e1c-other.sqlite.bz2"/>
        <timestamp>1657165688</timestamp>
        <size>2758</size>
        <open-size>32768</open-size>
        <database_version>10</database_version>
    </data>
    </repomd>
"""
).strip()

PRIMARY_XML = textwrap.dedent(
    """
<?xml version="1.0" encoding="UTF-8"?>
<metadata xmlns="http://linux.duke.edu/metadata/common" xmlns:rpm="http://linux.duke.edu/metadata/rpm" packages="5">
<package type="rpm">
  <name>wireplumber</name>
  <arch>x86_64</arch>
  <version epoch="0" ver="0.4.10" rel="1.fc36"/>
  <checksum type="sha256" pkgid="YES">539a773f3f39a7b2b5f971bdd0063f7d4201aab00920f380962e935356dc4d3a</checksum>
  <summary>A modular session/policy manager for PipeWire</summary>
  <description>WirePlumber is a modular session/policy manager for PipeWire and a
GObject-based high-level library that wraps PipeWire's API, providing
convenience for writing the daemon's modules as well as external tools for
managing PipeWire.</description>
  <packager>Fedora Project</packager>
  <url>https://pipewire.pages.freedesktop.org/wireplumber/</url>
  <time file="1657165671" build="1652194859"/>
  <size package="82141" installed="286454" archive="298004"/>
  <location href="packages/w/wireplumber-0.4.10-1.fc36.x86_64.rpm"/>
  <format>
    <rpm:license>MIT</rpm:license>
    <rpm:vendor>Fedora Project</rpm:vendor>
    <rpm:group>Unspecified</rpm:group>
    <rpm:buildhost>buildvm-x86-27.iad2.fedoraproject.org</rpm:buildhost>
    <rpm:sourcerpm>wireplumber-0.4.10-1.fc36.src.rpm</rpm:sourcerpm>
    <rpm:header-range start="4504" end="20677"/>
    <rpm:provides>
      <rpm:entry name="pipewire-session-manager"/>
      <rpm:entry name="wireplumber" flags="EQ" epoch="0" ver="0.4.10" rel="1.fc36"/>
      <rpm:entry name="wireplumber(x86-64)" flags="EQ" epoch="0" ver="0.4.10" rel="1.fc36"/>
    </rpm:provides>
    <rpm:requires>
      <rpm:entry name="/bin/sh"/>
      <rpm:entry name="libgcc_s.so.1()(64bit)"/>
      <rpm:entry name="libgcc_s.so.1(GCC_3.0)(64bit)"/>
      <rpm:entry name="libgcc_s.so.1(GCC_3.3.1)(64bit)"/>
      <rpm:entry name="libglib-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgobject-2.0.so.0()(64bit)"/>
      <rpm:entry name="libpipewire-0.3.so.0()(64bit)"/>
      <rpm:entry name="libwireplumber-0.4.so.0()(64bit)"/>
      <rpm:entry name="rtld(GNU_HASH)"/>
      <rpm:entry name="wireplumber-libs(x86-64)" flags="EQ" epoch="0" ver="0.4.10" rel="1.fc36"/>
      <rpm:entry name="libc.so.6(GLIBC_2.34)(64bit)"/>
    </rpm:requires>
    <rpm:conflicts>
      <rpm:entry name="pipewire-session-manager"/>
    </rpm:conflicts>
    <file type="dir">/etc/wireplumber</file>
    <file type="dir">/etc/wireplumber/bluetooth.lua.d</file>
    <file type="dir">/etc/wireplumber/common</file>
    <file type="dir">/etc/wireplumber/main.lua.d</file>
    <file type="dir">/etc/wireplumber/policy.lua.d</file>
    <file>/usr/bin/wireplumber</file>
    <file>/usr/bin/wpctl</file>
    <file>/usr/bin/wpexec</file>
  </format>
</package>
<package type="rpm">
  <name>wireplumber-libs</name>
  <arch>x86_64</arch>
  <version epoch="0" ver="0.4.10" rel="1.fc36"/>
  <checksum type="sha256" pkgid="YES">1f0d373bd1b8af6b4b7baab1c89e4820aa8cd8691f51fca4fccac9785fe715ea</checksum>
  <summary>Libraries for WirePlumber clients</summary>
  <description>This package contains the runtime libraries for any application that wishes
to interface with WirePlumber.</description>
  <packager>Fedora Project</packager>
  <url>https://pipewire.pages.freedesktop.org/wireplumber/</url>
  <time file="1657165671" build="1652194859"/>
  <size package="325613" installed="1188155" archive="1196460"/>
  <location href="packages/w/wireplumber-libs-0.4.10-1.fc36.x86_64.rpm"/>
  <format>
    <rpm:license>MIT</rpm:license>
    <rpm:vendor>Fedora Project</rpm:vendor>
    <rpm:group>Unspecified</rpm:group>
    <rpm:buildhost>buildvm-x86-27.iad2.fedoraproject.org</rpm:buildhost>
    <rpm:sourcerpm>wireplumber-0.4.10-1.fc36.src.rpm</rpm:sourcerpm>
    <rpm:header-range start="4504" end="20445"/>
    <rpm:provides>
      <rpm:entry name="libwireplumber-0.4.so.0()(64bit)"/>
      <rpm:entry name="libwireplumber-module-default-nodes-api.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-default-nodes.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-default-profile.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-file-monitor-api.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-logind.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-lua-scripting.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-metadata.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-mixer-api.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-portal-permissionstore.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-reserve-device.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-si-audio-adapter.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-si-audio-endpoint.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-si-node.so()(64bit)"/>
      <rpm:entry name="libwireplumber-module-si-standard-link.so()(64bit)"/>
      <rpm:entry name="wireplumber-libs" flags="EQ" epoch="0" ver="0.4.10" rel="1.fc36"/>
      <rpm:entry name="wireplumber-libs(x86-64)" flags="EQ" epoch="0" ver="0.4.10" rel="1.fc36"/>
    </rpm:provides>
    <rpm:requires>
      <rpm:entry name="libgcc_s.so.1()(64bit)"/>
      <rpm:entry name="libgcc_s.so.1(GCC_3.0)(64bit)"/>
      <rpm:entry name="libgcc_s.so.1(GCC_3.3.1)(64bit)"/>
      <rpm:entry name="libgio-2.0.so.0()(64bit)"/>
      <rpm:entry name="libglib-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgmodule-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgobject-2.0.so.0()(64bit)"/>
      <rpm:entry name="liblua-5.4.so()(64bit)"/>
      <rpm:entry name="libm.so.6()(64bit)"/>
      <rpm:entry name="libm.so.6(GLIBC_2.2.5)(64bit)"/>
      <rpm:entry name="libpipewire-0.3.so.0()(64bit)"/>
      <rpm:entry name="libsystemd.so.0()(64bit)"/>
      <rpm:entry name="libsystemd.so.0(LIBSYSTEMD_209)(64bit)"/>
      <rpm:entry name="rtld(GNU_HASH)"/>
      <rpm:entry name="libc.so.6(GLIBC_2.14)(64bit)"/>
    </rpm:requires>
    <rpm:recommends>
      <rpm:entry name="wireplumber(x86-64)" flags="EQ" epoch="0" ver="0.4.10" rel="1.fc36"/>
    </rpm:recommends>
  </format>
</package>
<package type="rpm">
  <name>xfce4-panel</name>
  <arch>x86_64</arch>
  <version epoch="0" ver="4.16.4" rel="1.fc36"/>
  <checksum type="sha256" pkgid="YES">1eecad127499d557f9d97562a1c65d9c881f3f63431546007a9ed714997b909c</checksum>
  <summary>Next generation panel for Xfce</summary>
  <description>This package includes the panel for the Xfce desktop environment.</description>
  <packager>Fedora Project</packager>
  <url>http://www.xfce.org/</url>
  <time file="1657165686" build="1650113596"/>
  <size package="1071292" installed="5255122" archive="5281072"/>
  <location href="packages/x/xfce4-panel-4.16.4-1.fc36.x86_64.rpm"/>
  <format>
    <rpm:license>GPLv2+ and LGPLv2+</rpm:license>
    <rpm:vendor>Fedora Project</rpm:vendor>
    <rpm:group>Unspecified</rpm:group>
    <rpm:buildhost>buildvm-x86-16.iad2.fedoraproject.org</rpm:buildhost>
    <rpm:sourcerpm>xfce4-panel-4.16.4-1.fc36.src.rpm</rpm:sourcerpm>
    <rpm:header-range start="4504" end="38505"/>
    <rpm:provides>
      <rpm:entry name="application()"/>
      <rpm:entry name="application(panel-desktop-handler.desktop)"/>
      <rpm:entry name="application(panel-preferences.desktop)"/>
      <rpm:entry name="config(xfce4-panel)" flags="EQ" epoch="0" ver="4.16.4" rel="1.fc36"/>
      <rpm:entry name="libxfce4panel-2.0.so.4()(64bit)"/>
      <rpm:entry name="mimehandler(application/x-desktop)"/>
      <rpm:entry name="xfce4-panel" flags="EQ" epoch="0" ver="4.16.4" rel="1.fc36"/>
      <rpm:entry name="xfce4-panel(x86-64)" flags="EQ" epoch="0" ver="4.16.4" rel="1.fc36"/>
    </rpm:provides>
    <rpm:requires>
      <rpm:entry name="/usr/bin/sh"/>
      <rpm:entry name="libX11.so.6()(64bit)"/>
      <rpm:entry name="libXext.so.6()(64bit)"/>
      <rpm:entry name="libatk-1.0.so.0()(64bit)"/>
      <rpm:entry name="libcairo-gobject.so.2()(64bit)"/>
      <rpm:entry name="libcairo.so.2()(64bit)"/>
      <rpm:entry name="libdbusmenu-glib.so.4()(64bit)"/>
      <rpm:entry name="libdbusmenu-gtk3.so.4()(64bit)"/>
      <rpm:entry name="libexo-2.so.0()(64bit)"/>
      <rpm:entry name="libgarcon-1.so.0()(64bit)"/>
      <rpm:entry name="libgarcon-gtk3-1.so.0()(64bit)"/>
      <rpm:entry name="libgdk-3.so.0()(64bit)"/>
      <rpm:entry name="libgdk_pixbuf-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgio-2.0.so.0()(64bit)"/>
      <rpm:entry name="libglib-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgmodule-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgobject-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgthread-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgtk-3.so.0()(64bit)"/>
      <rpm:entry name="libharfbuzz.so.0()(64bit)"/>
      <rpm:entry name="libm.so.6()(64bit)"/>
      <rpm:entry name="libm.so.6(GLIBC_2.2.5)(64bit)"/>
      <rpm:entry name="libpango-1.0.so.0()(64bit)"/>
      <rpm:entry name="libpangocairo-1.0.so.0()(64bit)"/>
      <rpm:entry name="libwnck-3.so.0()(64bit)"/>
      <rpm:entry name="libxfce4ui-2.so.0()(64bit)"/>
      <rpm:entry name="libxfce4util.so.7()(64bit)"/>
      <rpm:entry name="libxfconf-0.so.3()(64bit)"/>
      <rpm:entry name="libz.so.1()(64bit)"/>
      <rpm:entry name="rtld(GNU_HASH)"/>
      <rpm:entry name="libc.so.6(GLIBC_2.34)(64bit)"/>
    </rpm:requires>
    <rpm:obsoletes>
      <rpm:entry name="orage" flags="LT" epoch="0" ver="4.12.1" rel="17.fc34"/>
      <rpm:entry name="xfce4-cellmodem-plugin" flags="LT" epoch="0" ver="0.0.5" rel="29.fc34"/>
      <rpm:entry name="xfce4-embed-plugin" flags="LT" epoch="0" ver="1.6.0" rel="13.fc34"/>
      <rpm:entry name="xfce4-hardware-monitor-plugin" flags="LT" epoch="0" ver="1.6.0" rel="11"/>
      <rpm:entry name="xfce4-kbdleds-plugins" flags="LT" epoch="0" ver="0.0.6" rel="20.fc34"/>
    </rpm:obsoletes>
    <file>/etc/xdg/xfce4/panel/default.xml</file>
    <file>/usr/bin/xfce4-panel</file>
    <file>/usr/bin/xfce4-popup-applicationsmenu</file>
    <file>/usr/bin/xfce4-popup-directorymenu</file>
    <file>/usr/bin/xfce4-popup-windowmenu</file>
  </format>
</package>
<package type="rpm">
  <name>xfce4-power-manager</name>
  <arch>x86_64</arch>
  <version epoch="0" ver="4.16.0" rel="5.fc36"/>
  <checksum type="sha256" pkgid="YES">48697b6e83646e702d83523acd4a25df546129a1a11f3fbb81724c30d58e9c21</checksum>
  <summary>Power management for the Xfce desktop environment</summary>
  <description>Xfce Power Manager uses the information and facilities provided by HAL to
display icons and handle user callbacks in an interactive Xfce session.
Xfce Power Preferences allows authorised users to set policy and change
preferences.</description>
  <packager>Fedora Project</packager>
  <url>http://goodies.xfce.org/projects/applications/xfce4-power-manager</url>
  <time file="1657165686" build="1654865507"/>
  <size package="753300" installed="4646874" archive="4674064"/>
  <location href="packages/x/xfce4-power-manager-4.16.0-5.fc36.x86_64.rpm"/>
  <format>
    <rpm:license>GPLv2+</rpm:license>
    <rpm:vendor>Fedora Project</rpm:vendor>
    <rpm:group>Unspecified</rpm:group>
    <rpm:buildhost>buildvm-x86-21.iad2.fedoraproject.org</rpm:buildhost>
    <rpm:sourcerpm>xfce4-power-manager-4.16.0-5.fc36.src.rpm</rpm:sourcerpm>
    <rpm:header-range start="4504" end="36733"/>
    <rpm:provides>
      <rpm:entry name="application()"/>
      <rpm:entry name="application(xfce4-power-manager-settings.desktop)"/>
      <rpm:entry name="config(xfce4-power-manager)" flags="EQ" epoch="0" ver="4.16.0" rel="5.fc36"/>
      <rpm:entry name="libxfce4powermanager.so()(64bit)"/>
      <rpm:entry name="metainfo()"/>
      <rpm:entry name="metainfo(xfce4-power-manager.appdata.xml)"/>
      <rpm:entry name="xfce4-power-manager" flags="EQ" epoch="0" ver="4.16.0" rel="5.fc36"/>
      <rpm:entry name="xfce4-power-manager(x86-64)" flags="EQ" epoch="0" ver="4.16.0" rel="5.fc36"/>
    </rpm:provides>
    <rpm:requires>
      <rpm:entry name="libX11.so.6()(64bit)"/>
      <rpm:entry name="libXext.so.6()(64bit)"/>
      <rpm:entry name="libXrandr.so.2()(64bit)"/>
      <rpm:entry name="libatk-1.0.so.0()(64bit)"/>
      <rpm:entry name="libcairo-gobject.so.2()(64bit)"/>
      <rpm:entry name="libcairo.so.2()(64bit)"/>
      <rpm:entry name="libgdk-3.so.0()(64bit)"/>
      <rpm:entry name="libgdk_pixbuf-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgio-2.0.so.0()(64bit)"/>
      <rpm:entry name="libglib-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgmodule-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgobject-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgtk-3.so.0()(64bit)"/>
      <rpm:entry name="libharfbuzz.so.0()(64bit)"/>
      <rpm:entry name="libm.so.6()(64bit)"/>
      <rpm:entry name="libm.so.6(GLIBC_2.2.5)(64bit)"/>
      <rpm:entry name="libm.so.6(GLIBC_2.27)(64bit)"/>
      <rpm:entry name="libnotify.so.4()(64bit)"/>
      <rpm:entry name="libpango-1.0.so.0()(64bit)"/>
      <rpm:entry name="libpangocairo-1.0.so.0()(64bit)"/>
      <rpm:entry name="libupower-glib.so.3()(64bit)"/>
      <rpm:entry name="libxfce4panel-2.0.so.4()(64bit)"/>
      <rpm:entry name="libxfce4ui-2.so.0()(64bit)"/>
      <rpm:entry name="libxfce4util.so.7()(64bit)"/>
      <rpm:entry name="libxfconf-0.so.3()(64bit)"/>
      <rpm:entry name="libz.so.1()(64bit)"/>
      <rpm:entry name="polkit"/>
      <rpm:entry name="rtld(GNU_HASH)"/>
      <rpm:entry name="upower" flags="GE" epoch="0" ver="0.99"/>
      <rpm:entry name="xfce4-panel" flags="GE" epoch="0" ver="4.16"/>
      <rpm:entry name="libc.so.6(GLIBC_2.34)(64bit)"/>
    </rpm:requires>
    <file>/etc/xdg/autostart/xfce4-power-manager.desktop</file>
    <file>/etc/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-power-manager.xml</file>
    <file>/usr/bin/xfce4-power-manager</file>
    <file>/usr/bin/xfce4-power-manager-settings</file>
    <file>/usr/sbin/xfce4-pm-helper</file>
    <file>/usr/sbin/xfpm-power-backlight-helper</file>
  </format>
</package>
<package type="rpm">
  <name>xfce4-terminal</name>
  <arch>x86_64</arch>
  <version epoch="0" ver="1.0.3" rel="1.fc36"/>
  <checksum type="sha256" pkgid="YES">6b6d0d941c16988b4c68ae473f1af141dedafe691922c0c88f6f3ef82baeef79</checksum>
  <summary>Terminal Emulator for the Xfce Desktop environment</summary>
  <description>Xfce4-terminal is a lightweight and easy to use terminal emulator application
with many advanced features including drop down, tabs, unlimited scrolling,
full colors, fonts, transparent backgrounds, and more.</description>
  <packager>Fedora Project</packager>
  <url>http://docs.xfce.org/apps/terminal/start</url>
  <time file="1657165686" build="1652445299"/>
  <size package="711256" installed="3699394" archive="3715232"/>
  <location href="packages/x/xfce4-terminal-1.0.3-1.fc36.x86_64.rpm"/>
  <format>
    <rpm:license>GPLv2+</rpm:license>
    <rpm:vendor>Fedora Project</rpm:vendor>
    <rpm:group>Unspecified</rpm:group>
    <rpm:buildhost>buildvm-x86-15.iad2.fedoraproject.org</rpm:buildhost>
    <rpm:sourcerpm>xfce4-terminal-1.0.3-1.fc36.src.rpm</rpm:sourcerpm>
    <rpm:header-range start="4504" end="25361"/>
    <rpm:provides>
      <rpm:entry name="Terminal" flags="EQ" epoch="0" ver="1.0.3" rel="1.fc36"/>
      <rpm:entry name="application()"/>
      <rpm:entry name="application(xfce4-terminal-settings.desktop)"/>
      <rpm:entry name="application(xfce4-terminal.desktop)"/>
      <rpm:entry name="xfce4-terminal" flags="EQ" epoch="0" ver="1.0.3" rel="1.fc36"/>
      <rpm:entry name="xfce4-terminal(x86-64)" flags="EQ" epoch="0" ver="1.0.3" rel="1.fc36"/>
    </rpm:provides>
    <rpm:requires>
      <rpm:entry name="dejavu-sans-mono-fonts"/>
      <rpm:entry name="libX11.so.6()(64bit)"/>
      <rpm:entry name="libcairo.so.2()(64bit)"/>
      <rpm:entry name="libgdk-3.so.0()(64bit)"/>
      <rpm:entry name="libgdk_pixbuf-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgio-2.0.so.0()(64bit)"/>
      <rpm:entry name="libglib-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgobject-2.0.so.0()(64bit)"/>
      <rpm:entry name="libgtk-3.so.0()(64bit)"/>
      <rpm:entry name="libpango-1.0.so.0()(64bit)"/>
      <rpm:entry name="libvte-2.91.so.0()(64bit)"/>
      <rpm:entry name="libxfce4ui-2.so.0()(64bit)"/>
      <rpm:entry name="libxfce4util.so.7()(64bit)"/>
      <rpm:entry name="libxfconf-0.so.3()(64bit)"/>
      <rpm:entry name="rtld(GNU_HASH)"/>
      <rpm:entry name="libc.so.6(GLIBC_2.34)(64bit)"/>
    </rpm:requires>
    <rpm:obsoletes>
      <rpm:entry name="Terminal" flags="LT" epoch="0" ver="0.4.8" rel="5"/>
    </rpm:obsoletes>
    <file>/usr/bin/xfce4-terminal</file>
  </format>
</package>
</metadata>
"""
).strip()

TREEINFO = """[checksums]
images/boot.iso = sha256:f6be6ec48a4a610e25d591dcf98e1777c4274ed58c583fa64d0aea5b3ecffb18
images/efiboot.img = sha256:94d5500c4ba266ce77b06aa955d9041eea22129737badc6af56c283dcaec1c29
images/install.img = sha256:46171146377610cfa0deae157bbcc4ea146b3995c9b0c58d9f261ce404468abe
images/pxeboot/initrd.img = sha256:e0cd3966097c175d3aaf406a7f8c094374c69504c7be8f08d8084ab9a8812796
images/pxeboot/vmlinuz = sha256:370db9a3943d4f46dc079dbaeb7e0cc3910dca069f7eede66d3d7d0d5177f684

[general]
; WARNING.0 = This section provides compatibility with pre-productmd treeinfos.
; WARNING.1 = Read productmd documentation for details about new format.
arch = x86_64
family = Red Hat Enterprise Linux
name = Red Hat Enterprise Linux 8.0.0
packagedir = Packages
platforms = x86_64,xen
repository = .
timestamp = 1554367044
variant = BaseOS
variants = BaseOS
version = 8.0.0

[header]
type = productmd.treeinfo
version = 1.2

[images-x86_64]
boot.iso = images/boot.iso
efiboot.img = images/efiboot.img
initrd = images/pxeboot/initrd.img
kernel = images/pxeboot/vmlinuz

[images-xen]
initrd = images/pxeboot/initrd.img
kernel = images/pxeboot/vmlinuz

[release]
name = Red Hat Enterprise Linux
short = RHEL
version = 8.0.0

[stage2]
mainimage = images/install.img

[tree]
arch = x86_64
build_timestamp = 1554367044
platforms = x86_64,xen
variants = BaseOS

[variant-BaseOS]
id = BaseOS
name = BaseOS
packages = Packages
repository = .
type = variant
uid = BaseOS"""

TREEINFO_APPSTREAM = """[general]
; WARNING.0 = This section provides compatibility with pre-productmd treeinfos.
; WARNING.1 = Read productmd documentation for details about new format.
arch = x86_64
family = Red Hat Enterprise Linux
name = Red Hat Enterprise Linux 8.3
packagedir = Packages
platforms = x86_64
repository = .
timestamp = 1601410486
variant = AppStream
variants = AppStream
version = 8.3

[header]
type = productmd.treeinfo
version = 1.2

[release]
name = Red Hat Enterprise Linux
short = RHEL
version = 8.3

[tree]
arch = x86_64
build_timestamp = 1601410486
platforms = x86_64
variants = AppStream

[variant-AppStream]
id = AppStream
name = AppStream
packages = Packages
repository = .
type = variant
uid = AppStream"""

EXTRA_FILES_JSON = """{
    "data": [
        {
            "checksums": {
                "md5": "feb4d252ee63634debea654b446e830b",
                "sha1": "a73fad5aeb5642d1b2108885010c4e7a547a1204",
                "sha256": "c4117d0e325cde392981626edbd1484c751f0216689a171e4b7547e8800acc21"
            },
            "file": "RPM-GPG-KEY-redhat-release",
            "size": 5134
        },
        {
            "checksums": {
                "md5": "3c24137e12ece142a27bbf825c256936",
                "sha1": "a72daf8585b41529269cdffcca3a0b3d4e2f21cd",
                "sha256": "3f8644b35db4197e7689d0a034bdef2039d92e330e6b22217abfa6b86a1fc0fa"
            },
            "file": "RPM-GPG-KEY-redhat-beta",
            "size": 1669
        },
        {
            "checksums": {
                "md5": "b234ee4d69f5fce4486a80fdaf4a4263",
                "sha1": "4cc77b90af91e615a64ae04893fdffa7939db84c",
                "sha256": "8177f97513213526df2cf6184d8ff986c675afb514d4e68a404010521b880643"
            },
            "file": "GPL",
            "size": 18092
        },
        {
            "checksums": {
                "md5": "0c53898068810a989fa59ca0656bdf24",
                "sha1": "42d51858642b8a0d10fdf09050266395544ea556",
                "sha256": "8f833ce3fbcbcb82e47687a890c043332c88350ddabd606201556e14aaf8fcd9"
            },
            "file": "EULA",
            "size": 8154
        }
    ],
    "header": {
        "version": "1.0"
    }
}"""


class StaticFetcher:
    def __init__(self):
        self.content: dict[str, str] = {}

    async def __call__(self, url: str) -> Optional[BinaryIO]:
        out = self.content.get(url)
        if out is not None:
            # Since fetchers are allowed to return either str or an io stream,
            # this test wraps the canned strings into a stream (while some other
            # tests do not) to ensure both cases are covered.
            out = io.BytesIO(out.encode())
        return out


async def test_typical_index():
    fetcher = StaticFetcher()

    fetcher.content["https://example.com/repodata/repomd.xml"] = REPOMD_XML
    fetcher.content[
        "https://example.com/repodata/d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf-primary.xml.gz"
    ] = PRIMARY_XML
    fetcher.content["https://example.com/treeinfo"] = TREEINFO
    fetcher.content["https://example.com/extra_files.json"] = EXTRA_FILES_JSON

    entries: list[GeneratedIndex] = []
    async for entry in autoindex("https://example.com", fetcher=fetcher):
        print(f"Found one entry: {entry.relative_dir}")
        entries.append(entry)

    # It should generate some entries
    assert entries

    entries.sort(key=lambda e: e.relative_dir)

    # First check that the directory structure was reproduced.
    assert [e.relative_dir for e in entries] == [
        "",
        "images",
        "images/pxeboot",
        "packages",
        "packages/w",
        "packages/x",
        "repodata",
    ]

    by_relative_dir: dict[str, GeneratedIndex] = {}
    for entry in entries:
        by_relative_dir[entry.relative_dir] = entry

    # Sanity check a few links expected to appear in each.
    assert '<a href="repodata/">' in by_relative_dir[""].content
    assert '<a href="packages/">' in by_relative_dir[""].content

    assert '<a href="w/">' in by_relative_dir["packages"].content
    assert '<a href="x/">' in by_relative_dir["packages"].content

    assert '<a href="images/">' in by_relative_dir[""].content
    assert '<a href="pxeboot/">' in by_relative_dir["images"].content

    assert (
        '<a href="284769ec79daa9e0a3b0129bb6260cc6271c90c4fe02b43dfa7cdf7635fb803f-filelists.xml.gz">'
        in by_relative_dir["repodata"].content
    )

    assert (
        '<a href="wireplumber-libs-0.4.10-1.fc36.x86_64.rpm">'
        in by_relative_dir["packages/w"].content
    )
    assert (
        '<a href="xfce4-terminal-1.0.3-1.fc36.x86_64.rpm">'
        in by_relative_dir["packages/x"].content
    )

    assert '<a href="treeinfo">' in by_relative_dir[""].content

    assert '<a href="extra_files.json">' in by_relative_dir[""].content

    assert '<a href="EULA">' in by_relative_dir[""].content

    assert '<a href="GPL">' in by_relative_dir[""].content

    assert '<a href="RPM-GPG-KEY-redhat-beta">' in by_relative_dir[""].content

    assert '<a href="RPM-GPG-KEY-redhat-release">' in by_relative_dir[""].content

    assert '<a href="boot.iso">' in by_relative_dir["images"].content

    assert '<a href="install.img">' in by_relative_dir["images"].content

    assert '<a href="vmlinuz">' in by_relative_dir["images/pxeboot"].content

    # Sample the order of entries in some of the listings.
    # Directories are expected to come first.
    links = re.findall(r'<a href="([^"]+)"', by_relative_dir[""].content)
    assert links == [
        "images/",
        "packages/",
        "repodata/",
        "EULA",
        "GPL",
        "RPM-GPG-KEY-redhat-beta",
        "RPM-GPG-KEY-redhat-release",
        "extra_files.json",
        "treeinfo",
    ]

    links = re.findall(r'<a href="([^"]+)"', by_relative_dir["images"].content)
    assert links == [
        "../",
        "pxeboot/",
        "boot.iso",
        "efiboot.img",
        "install.img",
    ]


async def test_typical_appstream_index():
    fetcher = StaticFetcher()

    fetcher.content["https://example.com/repodata/repomd.xml"] = REPOMD_XML
    fetcher.content[
        "https://example.com/repodata/d4888f04f95ac067af4d997d35c6d345cbe398563d777d017a3634c9ed6148cf-primary.xml.gz"
    ] = PRIMARY_XML
    fetcher.content["https://example.com/treeinfo"] = TREEINFO_APPSTREAM
    fetcher.content["https://example.com/extra_files.json"] = EXTRA_FILES_JSON

    entries: list[GeneratedIndex] = []
    async for entry in autoindex("https://example.com", fetcher=fetcher):
        print(f"Found one entry: {entry.relative_dir}")
        entries.append(entry)

    # It should generate some entries
    assert entries

    entries.sort(key=lambda e: e.relative_dir)

    # First check that the directory structure was reproduced.
    assert [e.relative_dir for e in entries] == [
        "",
        "packages",
        "packages/w",
        "packages/x",
        "repodata",
    ]

    by_relative_dir: dict[str, GeneratedIndex] = {}
    for entry in entries:
        by_relative_dir[entry.relative_dir] = entry

    # Sanity check a few links expected to appear in each.
    assert '<a href="repodata/">' in by_relative_dir[""].content
    assert '<a href="packages/">' in by_relative_dir[""].content

    assert '<a href="w/">' in by_relative_dir["packages"].content
    assert '<a href="x/">' in by_relative_dir["packages"].content

    assert (
        '<a href="284769ec79daa9e0a3b0129bb6260cc6271c90c4fe02b43dfa7cdf7635fb803f-filelists.xml.gz">'
        in by_relative_dir["repodata"].content
    )

    assert (
        '<a href="wireplumber-libs-0.4.10-1.fc36.x86_64.rpm">'
        in by_relative_dir["packages/w"].content
    )
    assert (
        '<a href="xfce4-terminal-1.0.3-1.fc36.x86_64.rpm">'
        in by_relative_dir["packages/x"].content
    )

    assert '<a href="treeinfo">' in by_relative_dir[""].content

    assert '<a href="extra_files.json">' in by_relative_dir[""].content

    assert '<a href="EULA">' in by_relative_dir[""].content

    assert '<a href="GPL">' in by_relative_dir[""].content

    assert '<a href="RPM-GPG-KEY-redhat-beta">' in by_relative_dir[""].content

    assert '<a href="RPM-GPG-KEY-redhat-release">' in by_relative_dir[""].content
