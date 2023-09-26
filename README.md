# rocrate-to-sembench

Example workflow file:

```
on: [push]
jobs:
  job0:
    runs-on: ubuntu-latest
    steps:
      - name: checkout
        uses: actions/checkout@v3
      - name: rocrate-to-sembench
        uses: vliz-be-opsci/rocrate-to-sembench@main
        env:
          PROFILE: https://data.emobon.embrc.eu/observatory-profile/0.2
```

with:

* `PROFILE`: The rocrate profile URI to use in case a new rocrate needs to be instantiated.
