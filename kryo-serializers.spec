%global with_wicket 0
Name:          kryo-serializers
Version:       0.23
Release:       1%{?dist}
Summary:       Additional kryo serializers
License:       ASL 2.0
URL:           https://github.com/magro/kryo-serializers
Source0:       https://github.com/magro/%{name}/archive/%{name}-%{version}.tar.gz
BuildRequires: java-devel

BuildRequires: mvn(asm:asm)
BuildRequires: mvn(cglib:cglib)
BuildRequires: mvn(com.esotericsoftware.kryo:kryo)
BuildRequires: mvn(com.esotericsoftware.minlog:minlog)
BuildRequires: mvn(joda-time:joda-time)
BuildRequires: mvn(org.sonatype.oss:oss-parent)

%if %with_wicket
# Disable Apache Wicket support
# BuildRequires: mvn(org.apache.wicket:wicket:1.4.17)
BuildRequires: mvn(org.apache.wicket:wicket-core)
# Test deps
# BuildRequires: mvn(javax.servlet:servlet-api:2.5)
BuildRequires: mvn(org.jboss.spec.javax.servlet:jboss-servlet-api_2.5_spec)
%endif
BuildRequires: mvn(commons-lang:commons-lang)
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(org.objenesis:objenesis)
BuildRequires: mvn(org.slf4j:slf4j-api)
BuildRequires: mvn(org.slf4j:slf4j-simple)
BuildRequires: mvn(org.testng:testng)

BuildRequires: maven-local
BuildRequires: maven-plugin-bundle

BuildArch:     noarch

%description
Additional kryo (http://kryo.googlecode.com) serializers for
standard JDK types (e.g. currency, JDK proxies) and
some for external libraries (e.g. JODA TIME, CGLIB proxies, Wicket).

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}
find -name '*.class' -print -delete
find -name '*.jar' -print -delete

%pom_remove_plugin :findbugs-maven-plugin

%if !%with_wicket
%pom_remove_dep org.apache.wicket:wicket
%pom_remove_dep javax.servlet:servlet-api
rm -r src/main/java/de/javakaffee/kryoserializers/wicket \
 src/test/java/de/javakaffee/kryoserializers/wicket
%else
sed -i "s|<groupId>javax.servlet|<groupId>org.jboss.spec.javax.servlet|" pom.xml
sed -i "s|<artifactId>servlet-api|<artifactId>jboss-servlet-api_2.5_spec|" pom.xml
sed -i "s|<artifactId>wicket|<artifactId>wicket-core|" pom.xml
%endif

# package com.esotericsoftware.minlog does not exist
%pom_add_dep com.esotericsoftware.minlog:minlog::provided
# NoClassDefFoundError: org/objenesis/instantiator/ObjectInstantiator
%pom_add_dep org.objenesis:objenesis::test

%build

%mvn_file de.javakaffee:%{name} %{name}
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENCE.txt README.markdown

%files javadoc -f .mfiles-javadoc
%doc LICENCE.txt

%changelog
* Sun Sep 29 2013 gil cattaneo <puntogil@libero.it> 0.23-1
- initial rpm