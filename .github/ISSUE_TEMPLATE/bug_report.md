name: 🐛 Bug Report
description: Report a reproducible bug
title: "[Bug]: "
labels: [bug]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for helping improve this project! Please fill out the following information.

  - type: input
    id: environment
    attributes:
      label: Environment
      description: OS, Python version, browser, etc.
      placeholder: "e.g., Windows 11, Python 3.10"
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Bug Description
      description: A clear and concise description of what the bug is.
      placeholder: "When I try to ..., it crashes/gives unexpected result..."
    validations:
      required: true

  - type: textarea
    id: steps
    attributes:
      label: Steps to Reproduce
      description: List the exact steps to reproduce the issue.
      placeholder: |
        1. Go to '...'
        2. Click on '...'
        3. Scroll down to '...'
        4. See error
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Logs / Stack Trace
      description: Paste any logs or error output.
      render: shell
