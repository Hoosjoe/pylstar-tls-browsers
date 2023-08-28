# pylstar-tls

[pylstar](https://github.com/gbossert/pylstar) applied to TLS using [scapy](https://github.com/secdev/scapy).

## Installation

There are two ways to use `pylstar-tls`

  * directly on your system (you will need to install Python3 and the depdendencies in requirements.txt)
  * in a Docker container (using the Dockerfile in the repo)


## Nano-tutorial

Once you have installed `pylstar-tls`, you can infer a server
listening at `SERVER:PORT` using the `tls13` scenario with the
following command:

    src/infer_server.py -R SERVER:PORT -S tls13

The output will be put into `/tmp/tls_inferer` but you can
specify another directory using the `-o` option.


To infer a client, you first have to generate a valid RSA certificate
and private key, which we call `cert.pem` and `key.pem`.  Then, we can
run the tool using the following command:

    src/infer_client.py -L 127.0.0.1:4433 -C valid:cert.pem:key.pem:DEFAULT -S tls13

Finally, you have to repeatedly run the client against the endpoint
specified for the inference tool, e.g. for `openssl s_client`:

    while true; do openssl s_client -connect 127.0.0.1:4433; done


The output contains logs and the resulting state machine (the final
version is called `final.automaton`). To convert this file into a .dot
file, you can use the following command:

    src/automaton2dot.py server.tls13 final.automaton final.dot

where `server.tls13` are the role and the scenario you used for the
inference.


## Bugs and enhancements

Please, report any bug found by opening a ticket and/or by submiting a pull requests.


## Authors and acknowledgment

  * Aina Toky Rasoamanana
  * Olivier Levillain
  * Lorenzo Nadal Santa
  * Clément Parrsegny

This tool has been supported in part by the French ANR [GASP project](https://gasp.ebfe.fr) (ANR-19-CE39-0001).


## License

This software is licensed under the GPLv3 License. See the `COPYING.txt` file
in the top distribution directory for the full license text.
