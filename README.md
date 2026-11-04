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

- [FUEL Development Documentation](https://ukaea.github.io/fuel/dev/)

### Raising an issue

1. On the [Issues](https://github.com/ukaea/fuel/issues) tab, click **New issue**.
2. Choose the form that matches your request:

   | Form | Description | Title starts with |
   |---|---|---|
   | New term request form | A request for a new term to be added to the vocabulary. | `[NTR]` |
   | Term revision form | A request for an existing term to be changed or revised. | `[REV]` |
   | Term retirement or replacement form | A request for an existing term to be replaced or retired. | `[TR]` |
   | New competency question request form | Request to consider a new competency question. | `[NCQ]` |

3. Add a title after the prefix, fill in the form and click **Create**.

#### Labels

| Label | Description |
|---|---|
| `bug` | Something isn't working |
| `Competency Question` | Request to add a Competency Question |
| `Concept Modelling` | Modelling of a Concept from the Term list. For requesting a new term see "Term Request" |
| `documentation` | Improvements or additions to documentation |
| `duplicate` | This issue or pull request already exists |
| `Governance` | Governance questions |
| `invalid` | This doesn't seem right |
| `Term Addition` | New Term request |
| `Term Update` | Term Update request |
| `wontfix` | This will not be worked on |

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


