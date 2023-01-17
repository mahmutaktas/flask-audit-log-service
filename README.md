# FLASK AUDIT LOG SERVICE

## Overview

This project is an audit log service that provides an API for accepting event data sent by other systems, storing them and querying recorded event data by field values. It has been developed with Python Flask Framework and uses Postgresql and Elasticsearch for storing data. All incoming logs get validated for their event type then they’re stored to the Elasticsearch.

This document consists of four main sections.

These sections are:

<ul>
  <li>Application Layout</li>
  <li>Authentication</li>
  <li>Event Type Manager</li>
  <li>Event Log</li>
</ul>

You can find more on the documet in the [pdf file.](https://drive.google.com/uc?export=download&id=1BBQxYOl8oFygzMaYsQ5nj-7jfQ2mLAFH)
