### CI Status

**Dev:**  
![OWL DL Profile (dev)](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/agbeltran/21194e497875f56c63a36e638e5e7f6b/raw/fuel-ci-profile-dev.json)
![Reasoning (dev)](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/agbeltran/21194e497875f56c63a36e638e5e7f6b/raw/fuel-ci-reasoning-dev.json)

**Main:**  
![OWL DL Profile (main)](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/agbeltran/21194e497875f56c63a36e638e5e7f6b/raw/fuel-ci-profile-main.json)
![Reasoning (main)](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/agbeltran/21194e497875f56c63a36e638e5e7f6b/raw/fuel-ci-reasoning-main.json)


# FUsion Energy Lexicon (FUEL)

FUsion Energy Lexicon (FUEL) is an ontology for fusion energy data and processes.

FUEL is currently under development.

### Development version 

To check the development version, visit [FUEL Dev](https://ukaea.github.io/fuel/dev/)

### Stable version 

To check the stable version, visit [FUEL](https://ukaea.github.io/fuel/)

### Documentation

To check the latest release documentation, visit

-  [FUEL Latest Release Documentation](https://ukaea.github.io/fuel/docs/)

and for the development version visit

- [FUEL Development Documentation](https://ukaea.github.io/fuel/dev/docs/)

### License

The code in this repository is licensed under the [Apache License 2.0](LICENSE).
The ontology itself is licensed under the [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).


### Content Negotiation

The FUEL ontology supports content negotiation. You can retrieve the ontology in different formats by using the base URI `https://w3id.org/fuel/` and specifying the `Accept` header:

- **RDF/XML**: `application/rdf+xml`
- **Turtle**: `text/turtle`
- **JSON-LD**: `application/ld+json`
- **HTML**: `text/html`

For example, you can retrieve using the 'curl' commdand:

```
curl -L -H "Accept: application/rdf+xml" https://w3id.org/fuel

curl -L -H "Accept: text/turtle" https://w3id.org/fuel

curl -L -H "Accept: text/html" http://w3id.org/fuel
```


