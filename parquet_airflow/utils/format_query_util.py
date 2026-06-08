import re
from typing import Any, Dict, List, Tuple, Union


class QueryParamTransformer:
    """
    Transforma queries con parámetros estilo :parametro
    al formato requerido por cada motor.
    """
    PARAM_PATTERN = re.compile(r":([a-zA-Z_][a-zA-Z0-9_]*)")

    @classmethod
    def transform(cls, query:str, params:Dict[str, Any], engine:str)->Tuple[str, Union[Dict[str, Any], List[Any]]]:
        engine = engine.lower()
        qParams = cls.PARAM_PATTERN.findall(query)
        if not qParams:
            return query, params
        cls._validate_params(qParams, params)
        if engine == "postgres":
            return cls._to_postgres(query, params)
        if engine == "sqlserver":
            return cls._to_sqlserver(query, params, qParams)
        raise ValueError(f"Transform Query - Engine: {engine}")
    
    @classmethod
    def replace_params(cls, query:str, params:List, engine:str):
        engine = engine.lower()
        qParams = cls.PARAM_PATTERN.findall(query)
        if not qParams:
            return query, params
        params = dict(zip(qParams, params))     # qParams = keys, params = values
        cls._validate_params(qParams, params)
        if engine == "postgres":
            return cls._to_postgres(query, params)
        if engine == "sqlserver":
            return cls._to_sqlserver(query, params, qParams)
        raise ValueError(f"Replace Params: {engine} - {query[:15]}")

    @classmethod
    def _validate_params(cls, param_names: List[str], params: Dict[str, Any]) -> None:
        missing = set(param_names) - set(params.keys())
        if missing:
            raise ValueError(f"Faltan parámetros requeridos: {', '.join(missing)}")

    @classmethod
    def _to_postgres(cls, query: str, params: Dict[str, Any]):
        transformed_query = cls.PARAM_PATTERN.sub(
            lambda match: f"%({match.group(1)})s",
            query
        )
        return transformed_query, params

    @classmethod
    def _to_sqlserver(cls, query: str, params: Dict[str, Any], parmNames: List[str]):
        transformed_query = cls.PARAM_PATTERN.sub("?", query)
        ordered_params = [
            params[name]
            for name in parmNames
        ]
        return transformed_query, ordered_params
    
    
