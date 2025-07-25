name: 💡 Feature Request
description: Suggest a new feature or improvement
title: "[Feature]: "
labels: [enhancement]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for your suggestion! Please provide as much detail as possible.

  - type: input
    id: motivation
    attributes:
      label: Motivation
      placeholder: "This feature will help users to..."
    validations:
      required: true

  - type: textarea
    id: description
    attributes:
      label: Feature Description
      description: Describe the feature you want to see implemented.
    validations:
      required: true

  - type: textarea
    id: alternatives
    attributes:
      label: Alternatives Considered
      description: Have you tried any workarounds or other solutions?
      placeholder: "I tried ..., but it didn’t fully solve the problem."
