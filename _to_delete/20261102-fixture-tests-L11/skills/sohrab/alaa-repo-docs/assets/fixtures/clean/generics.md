# Generics

## Inline code

These three lines are quoted verbatim from alaa-golang. They are Go generic calls inside code
spans, not Markdown links, and a checker that reports them is producing false positives.

- and `httpkit.Bind[T](r)` requires the JSON content type,
- decode with `httpkit.Bind[T](r)` and return its error unchanged,
- `httpkit.BindWith[T](r, httpkit.AllowUnknownFields())` is the only sanctioned way.

~~~text
[not a link](./nowhere.md)
~~~
