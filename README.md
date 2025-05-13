# Project Timeline (Mermaid Gantt Chart)

```mermaid
gantt
    title Cell Analysis and Visualization Project
    dateFormat  YYYY-MM-DD
	excludes weekends tuesday,wednesday,saturday,sunday
    
    section Planning Phase
    Requirements gathering       :a1, 2025-05-16, 1d
    Technology selection         :a2, after a1, 2d
    Architecture design          :a3, after a1, 2d
    Environment setup            :a4, after a1, 2d

    section Development Phase
    Cell segmentation model      :b1, after a4, 5d
    ResNet training              :b2, after a4, 5d
    Web app basic structure      :b3, after a4, 5d
    Web app visualization        :b4, after a4, 5d
    Integration                  :b5, after a4, 5d
    
    section Testing Phase
    Model evaluation             :c1, after b1, 5d
    Web app testing              :c2, after b1, 5d
    Integration testing          :c3, after b1, 5d
    Optimization     :c4, after c3, 4d
    
    section Deployment Phase
    Documentation finalization   :d1, after c1, 4d
    Final system review          :d2, after c1, 1d
    Handover                     :d3, after d2, 1d
    
    section Milestones
    Architecture finalized       :milestone, m1, after a3, 0d
    Segmentation model complete  :milestone, m2, after b1, 0d
    ResNet model trained         :milestone, m3, after b2, 0d
    Web app functionality complete :milestone, m4, after b4, 0d
    Testing complete             :milestone, m5, after c4, 0d
    Project delivered            :milestone, m6, after d3, 0d
```


# design-patterns

[![Actions Status][actions-badge]][actions-link]
[![PyPI version][pypi-version]][pypi-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

Examples of software design patterns.

## Installation


Install [pixi](https://pixi.sh):

- Linux and MacOS
    ```bash
    curl -fsSL https://pixi.sh/install.sh | bash
    ```
- Windows (powershell)
    ```bash
    iwr -useb https://pixi.sh/install.ps1 | iex
    ```

Install the dependencies, including the dev dependencies
    ```bash
    pixi install --all
    ```
or install only the runtime dependencies
    ```bash
    pixi install --environment default
    ```


## Usage

Execute the main script with

    ```bash
    pixi run python my_file.py
    ```


## Documentation

Generate the documentation locally with

    ```bash
    pixi run -e dev mkdocs serve --watch ./
    ```


## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for instructions on how to contribute.

## License

Distributed under the terms of the [MIT license](LICENSE).
