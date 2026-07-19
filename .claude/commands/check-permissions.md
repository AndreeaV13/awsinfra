Verifica permisiunile AWS inainte de deploy:
1. Ruleaza `aws sts get-caller-identity` si confirma ca identitatea e corecta
2. Verifica ca rolul `github-actions-awsinfra-deploy` exista
3. Listeaza permisiunile rolului
4. Verifica ca toate template-urile CloudFormation sunt valide cu `aws cloudformation validate-template` pentru fiecare fisier din infra/
5. Raporteaza ce lipseste sau ce e gresit
6. Daca lipsesc permisiuni, propune si aplica fix-ul automat (actualizare policy cu stack-urile necesare)
