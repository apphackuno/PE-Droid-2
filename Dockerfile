FROM ubuntu:trusty
#FROM php:5.6-apache

# Install base packages
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -yq install \
        curl \
        apache2 \
        libapache2-mod-php5 \
        php5-mysql \
        php5-mcrypt \
        php5-gd \
        php5-curl \
        php-pear \
        php-apc \
        python \
	python-dev \
	python-pip \
	python-virtualenv \
	unzip \
	zip \
	lib32z1 \
	lib32ncurses5 \
	lib32stdc++6 \
	lib32bz2-1.0 -y \
	openjdk-7-jre-headless \
	openjdk-7-jdk \
	aspectj \
	libaspectj-java && \
	
    rm -rf /var/lib/apt/lists/* && \
    curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer
RUN pip install protobuf>=2.5.0
RUN /usr/sbin/php5enmod mcrypt
RUN echo "ServerName localhost" >> /etc/apache2/apache2.conf && \
    sed -i "s/variables_order.*/variables_order = \"EGPCS\"/g" /etc/php5/apache2/php.ini

ENV ALLOW_OVERRIDE **False**
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64/
ENV PATH $JAVA_HOME/bin:$PATH
ENV PATH=${PATH}:/var/www/html/PE-Droid/aspectj1.8/bin

# Add image configuration and scripts
ADD run.sh /run.sh
RUN chmod 755 /*.sh

# Configure /app folder with sample app
#RUN mkdir -p /app && rm -fr /var/www/html && ln -s /app /var/www/html
RUN mkdir -p /PE-Droid && rm -fr /var/www/html && ln -s /PE-Droid /var/www/html
#ADD PE-Droid/ /app
ADD . /PE-Droid

#CMD ["java", "-jar", "/PE-Droid/aspectj-1.8.1.jar"]

EXPOSE 80
WORKDIR /PE-Droid
CMD ["/run.sh"]
