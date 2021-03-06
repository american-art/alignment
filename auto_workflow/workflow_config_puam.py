#!/usr/bin/env python


import logging

LOG_LEVEL = logging.INFO
ZIP_OUTPUT = True

repo_name = 'puam'
repo_path = '../../aac-repos/' + repo_name
base_uri = 'http://data.americanartcollaborative.org/puam/'
context_uri = 'https://github.com/american-art/aac-alignment/blob/master/karma-context.json'
REPO_CONFIG = [
    {
        'path': repo_path,
        'name': 'apicongeography_birth',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E39_Actor1',
        'context_uri': context_uri,
        'model_file': 'apicongeography-birth-model.ttl',
        'input_file': 'apicongeography.json',
        'input_file_type': 'json',
        'output_file_name': 'apicongeography-birth',
        'additional_settings':{'rdf.generation.selection':'DEFAULT_TEST'}
    },
    {
        'path': repo_path,
        'name': 'apicongeography_death',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E39_Actor1',
        'context_uri': context_uri,
        'model_file': 'apicongeography-death-model.ttl',
        'input_file': 'apicongeography.json',
        'input_file_type': 'json',
        'output_file_name': 'apicongeography-death',
        'additional_settings':{'rdf.generation.selection':'DEFAULT_TEST'}
    },
    {
        'path': repo_path,
        'name': 'apiconstituents_american',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E39_Actor1',
        'context_uri': context_uri,
        'model_file': 'apiconstituents_american-model.ttl',
        'input_file': 'apiconstituents_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiconstituents_american',
        'num_partitions': 20
    },
    {
        'path': repo_path,
        'name': 'apiconuris',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E39_Actor1',
        'context_uri': context_uri,
        'model_file': 'apiconuris-model.ttl',
        'input_file': 'apiconuris.json',
        'input_file_type': 'json',
        'output_file_name': 'apiconuris'
    },
    {
        'path': repo_path,
        'name': 'apiobjconxrefs_american',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjconxrefs_american-model.ttl',
        'input_file': 'apiobjconxrefs_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiobjconxrefs_american'
    },
    {
        'path': repo_path,
        'name': 'apiobjdimxrefs_american',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjdimxrefs_american-model.ttl',
        'input_file': 'apiobjdimxrefs_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiobjdimxrefs_american'
    },
    {
        'path': repo_path,
        'name': 'apiobjects_american',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjects_american-model.ttl',
        'input_file': 'apiobjects_american.jl',
        'input_file_type': 'jsonlines',
        'output_file_name': 'apiobjects_american'
    },
    {
        'path': repo_path,
        'name': 'apiobjtitlexrefs_american_primary_titles',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjtitlexrefs_american-primary_title-model.ttl',
        'input_file': 'apiobjtitlexrefs_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiobjtitlexrefs_american-primary_title',
        'additional_settings':{'rdf.generation.selection':'DEFAULT_TEST'}
    },
    {
        'path': repo_path,
        'name': 'apiobjtitlexrefs_american_other_titles',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjtitlexrefs_american-other_titles-model.ttl',
        'input_file': 'apiobjtitlexrefs_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiobjtitlexrefs_american-other_titles',
        'additional_settings':{'rdf.generation.selection':'DEFAULT_TEST'}
    },
    {
        'path': repo_path,
        'name': 'apiobjtitlexrefs_american_unknown_titles',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjtitlexrefs_american-unknown_title-model.ttl',
        'input_file': 'apiobjtitlexrefs_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiobjtitlexrefs_american-unknown_title',
        'additional_settings':{'rdf.generation.selection':'DEFAULT_TEST'}
    },
    {
        'path': repo_path,
        'name': 'apiobjgeograph_american',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjgeograph_american-model.ttl',
        'input_file': 'apiobjgeograph_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiobjgeograph_american',
    },
    {
        'path': repo_path,
        'name': 'apiobjmediaxrefs_american',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjmediaxrefs_american-model.ttl',
        'input_file': 'apiobjmediaxrefs_american.json',
        'input_file_type': 'json',
        'output_file_name': 'apiobjmediaxrefs_american',
    },
    {
        'path': repo_path,
        'name': 'apiobjtermsxrefs_american',
        'base_uri': base_uri,
        'rdf_root_uri': 'http://www.cidoc-crm.org/cidoc-crm/E22_Man-Made_Object1',
        'context_uri': context_uri,
        'model_file': 'apiobjtermsxrefs_american-model.ttl',
        'input_file': 'apiobjtermsxrefs_american.json.jl',
        'input_file_type': 'jsonlines',
        'output_file_name': 'apiobjtermsxrefs_american',
        'num_partitions': 20
    },
    {
       'path': repo_path,
       'name': 'PUAM_AAC_VoIDDescription',
       'base_uri': base_uri,
       'rdf_root_uri': 'http://rdfs.org/ns/void#DatasetDescription1',
       'context_uri': context_uri,
       'model_file': 'PUAM_Metadata-model.ttl',
       'input_file': 'PUAM_Metadata.json',
       'input_file_type': 'json',
       'output_file_name': 'PUAM_Metadata'
    }
]
