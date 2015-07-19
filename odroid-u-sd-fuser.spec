Name:           odroid-u-sd-fuser
Version:        0.1.0
Release:        1%{?dist}
Summary:        Boot media blob for ODROID-U2/U3/X2

Group:          System Environment/Base
License:        BSD
URL:            http://odroid.com/dokuwiki/doku.php?id=en:odroid-u3
Source0:        https://github.com/hardkernel/u-boot/raw/odroid-v2010.12/sd_fuse/bl1.HardKernel
Source1:        https://github.com/hardkernel/u-boot/raw/odroid-v2010.12/sd_fuse/bl2.HardKernel
Source2:        https://github.com/hardkernel/u-boot/raw/odroid-v2010.12/sd_fuse/tzsw.HardKernel
Source3:        odroid-u-sd-fuser
Source4:        odroid-u-emmc-fuser

BuildArch:      noarch

BuildRequires:  odroid-u-uboot

%description
Binary blob used to boot Hardkernel's ODROID-U2/U3/X2. The blob contains:
- bl1
- bl2
- u-boot
- TrustZone

%prep
cp -a %{SOURCE3} odroid-u-sd-fuser
cp -a %{SOURCE4} odroid-u-emmc-fuser

%build
signed_bl1_position=0
bl2_position=30
uboot_position=62
tzsw_position=2110

#<BL1 fusing>
echo "BL1 fusing"
dd oflag=dsync if=%{SOURCE0} of=bootblob.bin seek=$signed_bl1_position
#<BL2 fusing>
echo "BL2 fusing"
dd if=%{SOURCE1} of=bootblob.bin seek=$bl2_position
#<u-boot fusing>
echo "u-boot fusing"
dd if=/boot/uboot/u-boot.bin of=bootblob.bin seek=$uboot_position
#<TrustZone S/W fusing>
echo "TrustZone S/W fusing"
dd if=%{SOURCE2} of=bootblob.bin seek=$tzsw_position

chmod +x bootblob.bin

sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-u-sd-fuser
sed -i 's!@bootblobpath@!%{_datadir}/%{name}/bootblob.bin!g' odroid-u-emmc-fuser

%install
install -p -m0755 -D bootblob.bin %{buildroot}%{_datadir}/%{name}/bootblob.bin
install -p -m0755 -D odroid-u-sd-fuser %{buildroot}%{_bindir}/odroid-u-sd-fuser
install -p -m0755 -D odroid-u-emmc-fuser %{buildroot}%{_bindir}/odroid-u-emmc-fuser

%files
%{_bindir}/odroid-u-sd-fuser
%{_bindir}/odroid-u-emmc-fuser
%{_datadir}/%{name}/bootblob.bin

%changelog
* Sun Jul 19 2015 Scott K Logan <logans@cottsay.net> - 0.1.0-1
- Initial package
