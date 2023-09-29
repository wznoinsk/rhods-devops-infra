#!/bin/bash

unset AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY
unset AWS_SESSION_TOKEN

MFA_DEVICE_ARN=arn:aws:iam::585132637328:mfa/OTP
MFA_TOKEN=$1

credentials=$(aws sts get-session-token --serial-number $MFA_DEVICE_ARN --token-code $MFA_TOKEN --duration-seconds 86400)
export AWS_ACCESS_KEY_ID=$(echo $credentials | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo $credentials | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo $credentials | jq -r '.Credentials.SessionToken')

