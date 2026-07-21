# Instructiuni pentru Claude Code

## Regula principala - INAINTE DE ORICE PUSH

Inainte de a rula orice comanda git push sau de a sugera un push, INTOTDEAUNA:

1. Verifica identitatea AWS: `aws sts get-caller-identity`
2. Verifica permisiunile rolului `github-actions-awsinfra-deploy`:
   - `aws iam list-attached-role-policies --role-name github-actions-awsinfra-deploy`
   - `aws iam list-role-policies --role-name github-actions-awsinfra-deploy`
3. Verifica ca rolul are TOATE aceste permisiuni:
   - cloudformation:* pe stack-urile: network-stack, compute-stack, site-stack
   - ec2:* (inclusiv StopInstances, StartInstances, DescribeInstances)
   - s3:*
   - cloudfront:*
4. Daca lipseste orice permisiune, adaug-o automat la policy inainte de push
5. Valideaza toate template-urile din infra/
6. Doar dupa ce TOTUL e ok, permite push-ul

## Daca un stack e in stare de eroare

Daca vreun stack e in UPDATE_ROLLBACK_FAILED sau ROLLBACK_FAILED:
1. Ruleaza automat continue-update-rollback
2. Sau sterge si recreaza stack-ul daca e necesar
3. Nu da push pana nu e rezolvat

## Regiunea AWS

Intotdeauna foloseste regiunea: eu-central-1
