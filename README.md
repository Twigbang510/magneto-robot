# Magneto Robot

This project is a automation system built using [Robot Framework](https://robotframework.org/). It performs tasks like logging into the Magento website, filtering products, adding items to the cart, checking out, and saving order information.

## Table of Contents

- [Introduction](#introduction)
- [Folder Structure](#folder-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
---

### Introduction

This project automates the process of logging into a Magento site, filtering and selecting products based on criteria like category, size, and color, adding items to the cart, checking out, and saving order details to a file.

### Folder Structure

- **tasks.robot**: Contains the main automation scripts written in Robot Framework.
- **resources/**: Contains custom keywords like `driver_manager.py`, `sign_in.py`, and other modules to support automation tasks.
- **data/**: Stores data files like `order_detail.xlsx` to save order information.
- **output/**: Stores reports and logs generated after running the script.
- **README.md**: Documentation for using this project.

### Requirements

1. **Python** (version 3.9.13)
2. **Robot Framework** and necessary libraries
3. **Selenium libraries** to control the browser

### Installation

1. **Clone** this repository:

    ```bash
    git clone https://github.com/Twigbang510/magneto-robot.git
    cd your-repo-name
    ```

2. **Excel Setup**: Make sure `order_detail.xlsx` exists in the `data/` folder or is prepared to store order data.

### Usage

1. **Run the Robot Framework script**:

    ```bash
    python -m robot --report NONE --outputdir output --logtitle "Task log" tasks.robot
    ```

2. **Input Parameters**:
   - `email`, `password`: Provided from `Asset` or configured directly in the script.
   - `category`, `size`, `color`, `min price`, `max price`: Input parameters for filtering products. The system will log an error and stop if these are missing.
