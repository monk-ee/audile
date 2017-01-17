#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
"""
Created on 17 Jan 2017
@author: Monkee Magic
"""
__author__ = 'Monkee Magic <magic.monkee.magic@gmail.com>'
__version__ = '0.0.1'
__source__ = 'https://github.com/monkee/audile.git'

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

try:
    client = boto3.client('polly',region_name='us-east-1', verify=True)
    f = open('test_books/first_lensman_chapter_one.txt','r')
    text = f.read()
    f.close()

    print(len(text))

    response = client.synthesize_speech(
        OutputFormat='mp3',
        Text=text[:1500],
        TextType='text',
        VoiceId='Geraint'
    )

except (BotoCoreError, ClientError) as error:
    # The service returned an error, exit gracefully
    print(error)
    sys.exit(-1)
except Exception as e:
    print(e)
    sys.exit(-1)

if "AudioStream" in response:
    # Note: Closing the stream is important as the service throttles on the
    # number of parallel connections. Here we are using contextlib.closing to
    # ensure the close method of the stream object will be calledautomatically
    # at the end of the with statement's scope.
    with closing(response["AudioStream"]) as stream:
        output = os.path.join(gettempdir(), "speech.mp3")
        try:
            # Open a file for writing the output as a binary stream
            with open(output, "wb") as file:
                file.write(stream.read())
        except IOError as error:
            # Could not write to file, exit gracefully
            print(error)
            sys.exit(-1)
else:
    # The response didn't contain audio data, exit gracefully
    print("Could not stream audio")

