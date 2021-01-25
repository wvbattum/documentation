# IRMA Authentication
**NOTE**: IRMA authentication is NOT supported, you are on your own!

**NOTE**: The IRMA server is NOT part of the VPN software packages. YOU are responsible for its installation, configuration, installing updates, keep it secure and in general keep it running!

**NOTE**: IRMA authentication is NOT production ready! Check the bottom of this document for open issues.
___
## IRMA Server Configuration
First, download the IRMA server according to the documentation from the [IRMA documentation](https://irma.app/docs/getting-started/). Then, create the IRMA configuration file as follows:
```yml
production: true
no_email: true

# this is the URL used by the app to connect to the IRMA-go server through the
# (reverse) proxy
url: "https://vpn.example/irma"
port: 8088

requestors:
  myapp:
    disclose_perms: [ "{attribute}" ]
    sign_perms: []
    auth_method: "token"
    key: "{mysecrettoken}"
```
The file can be named as one pleases but has to have the `.yml` extension.

The variables mean the following:
* `production`: Setting this to true means that the default configurations for the other options are stricter.
* `port`: The port on which the server can be found.
* `url`: The url on which the server can be found.
* `disclose_perms`: The attributes the application that uses the specified `key` are allowed to disclose. Where `{attribute}` is the identifier of the particular attribute. All the identifiers can be found [here](https://privacybydesign.foundation/attribute-index/en/pbdf.html) under their Issuer &#8594; Credentials.
* `sign_perms`: The attributes the server is allowed to use to sign documents.
* `auth_method`: Specifies the authentication method. In the case of eduVPN this has to be `token`.
* `key`: Specifies the key that the eduVPN server has to send in the initial POST-request authentication header in order to be allowed to connect to the server. This token can be whatever you want. It only needs to match the token in the eduVPN configuration.

If you have the IRMA server installed from source, the configuration file must be in the `irmago` directory. Furthermore, if you want to start the server, you have to change your working directory to `irmago` and start the server with the following command:
```sh
$ go run ./irma server -c irma_configuration_file.yml
```

If you have installed the IRMA server using the prebuilt binary, the configuration file has to be placed in the same directory from which you are starting the server. Then to start the server, use the following command:
```sh
$ irma server -c irma_configuration_file.yml
```
 If you want to add verbosity, you can add the options `-v` or `-vv`.

## Portal Configuration
First, install the environment for your OS and follow the instructions from the "Base Deploy" and "Web Server Certificates" sections:  [Fedora](https://github.com/eduvpn/documentation/blob/v2/DEPLOY_FEDORA.md), [Debian](https://github.com/eduvpn/documentation/blob/v2/DEPLOY_DEBIAN.md), or [CentOS](https://github.com/eduvpn/documentation/blob/v2/DEPLOY_CENTOS.md).

If you have the environment installed, change the `config.php` file in the  `/etc/vpn-user-portal/` directory:

First, comment the line:
```php
'authMethod' => 'FormPdoAuthentication',        // PDO (database)
```
Then, add the following lines:
```php
'authMethod' => 'IrmaAuthentication',
'IrmaAuthentication' => [
    'irmaServerUrl' => 'http://localhost:8088',
    'userIdAttribute' => 'pbdf.sidn-pbdf.email.email',
    'secretToken' => 'mysecrettoken',
],
```
The variables mean the following:
   * `authMethod`: The authentication method the VPN service has to use. In our case: IRMA.
   * `irmaServerUrl`: The address on which the VPN server can find your IRMA server.
   * `userIdAttribute`: This is the attribute that the server has to verify.
   * `secretToken`: This is the token is used to let the server identify itself to the IRMA server.

Second, you have to change the Apache configuration file to configure the reverse proxy. Change the following file: `/etc/httpd/conf.d/{your_host_name}.conf`. You need to add the following lines to the HTTPS `VirtualHost`:
```sh
ProxyPass "/irma/"  "http://localhost:8088/irma/"
```

At last run the following command:
```
$ sudo systemctl restart httpd
```
