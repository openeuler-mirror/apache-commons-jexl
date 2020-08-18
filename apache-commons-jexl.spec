%global jarname commons-jexl
%global compatver 2.1.0
Name:                apache-%{jarname}
Version:             2.1.1
Release:             1
Summary:             Java Expression Language (JEXL)
License:             ASL 2.0
URL:                 http://commons.apache.org/jexl
Source0:             http://www.apache.org/dist/commons/jexl/source/%{jarname}-%{version}-src.tar.gz
Patch0:              001-Fix-tests.patch
Patch1:              apache-commons-jexl-javadoc.patch
Patch2:              0001-Port-to-current-javacc.patch
BuildRequires:       maven-local mvn(commons-logging:commons-logging) mvn(junit:junit)
BuildRequires:       mvn(org.apache.commons:commons-parent:pom:)
BuildRequires:       mvn(org.codehaus.mojo:javacc-maven-plugin)
Provides:            %{jarname} = %{version}-%{release}
BuildArch:           noarch

%description
Java Expression Language (JEXL) is an expression language engine which can be
embedded in applications and frameworks.  JEXL is inspired by Jakarta Velocity
and the Expression Language defined in the JavaServer Pages Standard Tag
Library version 1.1 (JSTL) and JavaServer Pages version 2.0 (JSP).  While
inspired by JSTL EL, it must be noted that JEXL is not a compatible
implementation of EL as defined in JSTL 1.1 (JSR-052) or JSP 2.0 (JSR-152).
For a compatible implementation of these specifications, see the Commons EL
project.
JEXL attempts to bring some of the lessons learned by the Velocity community
about expression languages in templating to a wider audience.  Commons Jelly
needed Velocity-ish method access, it just had to have it.

%package javadoc
Summary:             Javadocs for %{name}
Requires:            jpackage-utils
Provides:            %{jarname}-javadoc = %{version}-%{release}
%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{jarname}-%{version}-src
%patch0 -p1 -b .test
%patch1 -p1 -b .javadoc
%patch2 -p1
%pom_remove_dep org.apache.bsf:bsf-api
find \( -name '*.jar' -o -name '*.class' \) -delete
find -name '*.txt' -exec sed -i 's/\r//' '{}' +
%pom_xpath_set "pom:project/pom:version" %{compatver} jexl2-compat
%pom_xpath_set "pom:dependency[pom:artifactId='commons-jexl']/pom:version" %{version} jexl2-compat
echo "
<project>
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.fedoraproject</groupId>
  <artifactId>commons-jexl-aggegator</artifactId>
  <version>%{version}</version>
  <packaging>pom</packaging>
  <modules>
    <module>.</module>
    <module>jexl2-compat</module>
  </modules>
</project>" >>aggregator-pom.xml
%mvn_package :commons-jexl-aggegator __noinstall

%build
%mvn_build -- -f aggregator-pom.xml

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt RELEASE-NOTES.txt
%{_javadir}/%{name}

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Mon Jul 27 2020 chengzihan <chengzihan2@huawei.com> - 2.1.1-1
- Package init
