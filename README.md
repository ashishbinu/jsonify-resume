# jsonify-resume

[![License](https://img.shields.io/github/license/ashishbinu/jsonify-resume.svg)](https://github.com/ashishbinu/jsonify-resume/blob/main/LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/ashishbinu/jsonify-resume.svg)](https://github.com/ashishbinu/jsonify-resume/stargazers)
[![GitHub Issues](https://img.shields.io/github/issues/ashishbinu/jsonify-resume.svg)](https://github.com/ashishbinu/jsonify-resume/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/ashishbinu/jsonify-resume.svg)](https://github.com/ashishbinu/jsonify-resume/pulls)

**jsonify-resume** is a command-line tool that converts resumes into JSON Resume schema. Use this tool to save time on the conversion process.

## Installation

To get started, install Jsonify-Resume using the following command:

```bash
pipx install jsonify-resume
```

## Usage

1. **Configure Access Token**: Before using Jsonify-Resume, set your [OpenAI access token](https://chat.openai.com/api/auth/session) as an environment variable:

   ```bash
   export OPENAI_ACCESS_TOKEN=<YOUR_ACCESS_TOKEN>
   ```

2. **Conversion Process**:

   Use the following command to convert your resume (in PDF format) to JSON:

   ```bash
   jsonify-resume resume.pdf > resume.json
   ```

## Contributing

Found a bug or have a feature in mind? [Open an issue](https://github.com/ashishbinu/jsonify-resume/issues). To contribute, fork the repo, make changes, and submit a PR.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

This project relies on the [revchatgpt](https://github.com/acheong08/ChatGPT). Thanks to the developers of revchatgpt.

---

**jsonify-resume** is maintained by [@ashishbinu](https://github.com/ashishbinu). Connect with me on [Twitter](https://twitter.com/binu_ashish).
