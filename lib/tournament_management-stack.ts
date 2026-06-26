import { Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as cdk from 'aws-cdk-lib';
import * as path from 'path';
export class TournamentManagementStack extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);
    // 👇 IAM Role
    const teemsManagerRole= iam.Role.fromRoleArn(
      this,
      'teems-manager-role',
      `arn:aws:iam::695867875070:role/teems-manager-role`,
      {mutable: false},
    );

    // 👇 SecretManager
    const groupManagerSecret = secretsmanager.Secret.fromSecretAttributes(this, "prod/groupmanager", {
      secretCompleteArn:
        "arn:aws:secretsmanager:us-east-1:695867875070:secret:prod/groupmanager-N86lse"
    });

    // 👇 Lambda Layers
    const dotenv_layer = lambda.LayerVersion.fromLayerVersionArn(this, 'layerversion', 'arn:aws:lambda:us-east-1:695867875070:layer:dotenv-layer:2');
    const gql_layer = lambda.LayerVersion.fromLayerVersionArn(this, 'layerversion1', 'arn:aws:lambda:us-east-1:695867875070:layer:gql-layer:1');
    const requests_layer = lambda.LayerVersion.fromLayerVersionArn(this, 'layerversion2', 'arn:aws:lambda:us-east-1:695867875070:layer:requests-layer:1');
    const requeststoolbelt_layer = lambda.LayerVersion.fromLayerVersionArn(this, 'layerversion3', 'arn:aws:lambda:us-east-1:695867875070:layer:requests-toolbelt-layer:1');
    const aws4auth_layer = lambda.LayerVersion.fromLayerVersionArn(this, 'layerversion4', 'arn:aws:lambda:us-east-1:695867875070:layer:requests-aws4auth-layer:1');
    const requestsAwsSign_layer = lambda.LayerVersion.fromLayerVersionArn(this, 'layerversion5', 'arn:aws:lambda:us-east-1:695867875070:layer:requests_aws_sign:1');

    // Example - lambda function
    const startTournament_lambda = new lambda.Function(this,
      'startTournamentHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(60),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.startTournamentHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const completeTournament_lambda = new lambda.Function(this,
      'completeTournamentHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(60),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.completeTournamentHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });
    
    const getEventCompetitors_lambda = new lambda.Function(this, 'getEventCompetitorsHandler', {
      runtime: lambda.Runtime.PYTHON_3_9,
      timeout: cdk.Duration.seconds(20),
      code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
      handler: 'Lambda.TournamentStateManager.getEventCompetitorsHandler',
      layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
      role: teemsManagerRole,
      environment: {
        "region": this.region,
        "secretName": groupManagerSecret.secretName,
      }
    });

    const freeJudgeHandler_lambda = new lambda.Function(this,
      'freeJudgeHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(20),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.freeJudgeHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const useJudgeHandler_lambda = new lambda.Function(this,
      'useJudgeHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(20),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.useJudgeHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const startRoomHandler_lambda = new lambda.Function(this,
      'startRoomHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(20),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.startRoomHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const completeRoomHandler_lambda = new lambda.Function(this,
      'completeRoomHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(20),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.completeRoomHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const getAvailableJudgesHandler_lambda = new lambda.Function(this,
      'getAvailableJudgesHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(30),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.getAvailableJudgesHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const getAvailableRoomsHandler_lambda = new lambda.Function(this,
      'getAvailableRoomsHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(20),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.getAvailableRoomsHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const startEventHandler_lambda = new lambda.Function(this,
      'startEventHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(20),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.startEventHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });

    const completeEventHandler_lambda = new lambda.Function(this,
      'completeEventHandler', {
        runtime: lambda.Runtime.PYTHON_3_9,
        timeout: cdk.Duration.seconds(20),
        code: lambda.Code.fromAsset(path.join(__dirname, '/../src')),
        handler: 'Lambda.TournamentStateManager.completeEventHandler',
        layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, requestsAwsSign_layer],
        role: teemsManagerRole,
        environment: {
          "region": this.region,
          "secretName": groupManagerSecret.secretName,
        }
      });
    const startGroups_lambda = new lambda.Function(this, 'startGroupsHandler', {
      runtime: lambda.Runtime.PYTHON_3_9,
      timeout: cdk.Duration.seconds(60),
      code: lambda.Code.fromAsset(path.join(__dirname, `/../src`)), // where your lambda code located
      handler: 'Lambda.GroupManager.startGroups_handler', // file name . function name
      layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, aws4auth_layer],
      role: teemsManagerRole,
      environment: {
        "region": this.region,
        "secretName": groupManagerSecret.secretName,
      }
    });

    const startCompetition_lambda = new lambda.Function(this, 'startCompetitionHandler', {
      runtime: lambda.Runtime.PYTHON_3_9,
      timeout: cdk.Duration.seconds(30),
      code: lambda.Code.fromAsset(path.join(__dirname, `/../src`)), // where your lambda code located
      handler: 'Lambda.GroupManager.startCompetition_handler', // file name . function name
      layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, aws4auth_layer],
      role: teemsManagerRole,
      environment: {
        "region": this.region,
        "secretName": groupManagerSecret.secretName,
        //'table' : example_DB.tableName
      }
    });

    const collectResult_lambda = new lambda.Function(this, 'collectResultHandler', {
      runtime: lambda.Runtime.PYTHON_3_9,
      timeout: cdk.Duration.seconds(60),
      code: lambda.Code.fromAsset(path.join(__dirname, `/../src`)), // where your lambda code located
      handler: 'Lambda.GroupManager.collectResult_handler', // file name . function name
      layers: [dotenv_layer, gql_layer, requests_layer, requeststoolbelt_layer, aws4auth_layer],
      role: teemsManagerRole,
      environment: {
        "region": this.region,
        "secretName": groupManagerSecret.secretName,
      }
    });

    // Example - Api gateway
    // == 1. initialize apigw == 
    const teems_group_manager_api = new apigateway.RestApi(this, 'teems_groupmanager_api', {
      description: 'teems_groupmanager_api',
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
      }
    });
    //new cdk.CfnOutput(this, 'apiUrl', {value: teems_group_manager_api.url});
    // == 2. add resource '/example' == 
    const teems_group_manager_api_result = teems_group_manager_api.root.addResource('result');
    const teems_group_manager_api_startCompetition = teems_group_manager_api.root.addResource('startCompetition');
    const teems_group_manager_api_startGroups = teems_group_manager_api.root.addResource('startGroup');
    
    // == 3. intergrate rescore with lambda function ==
    teems_group_manager_api_result.addMethod(
      'POST',
      new apigateway.LambdaIntegration(collectResult_lambda, { proxy: true })
    )
    teems_group_manager_api_startCompetition.addMethod(
      'POST',
      new apigateway.LambdaIntegration(startCompetition_lambda, { proxy: true })
    )
    teems_group_manager_api_startGroups.addMethod(
      'POST',
      new apigateway.LambdaIntegration(startGroups_lambda, { proxy: true })
    )
    
    // == 1. initialize apigw == 
    const teems_tournament_state_manager_api = new apigateway.RestApi(this, 'teems_tournament_state_manager_api', {
      description: 'teems_tournament_state_manager_api',
      defaultCorsPreflightOptions: {
        allowOrigins: ['*'],
        allowCredentials: true
      }
    });
    //new cdk.CfnOutput(this, 'apiUrl', {value: teems_group_manager_api.url});
    // == 2. add resource '/example' == 
    const teems_tournament_state_manager_api_startEvent = teems_tournament_state_manager_api.root.addResource('startEvent');
    const teems_tournament_state_manager_api_completeEvent = teems_tournament_state_manager_api.root.addResource('completeEvent');
    const teems_tournament_state_manager_api_startTournament = teems_tournament_state_manager_api.root.addResource('startTournament');
    const teems_tournament_state_manager_api_completeTournament = teems_tournament_state_manager_api.root.addResource('completeTournament');
    const teems_tournament_state_manager_api_useJudge = teems_tournament_state_manager_api.root.addResource('useJudge');
    const teems_tournament_state_manager_api_freeJudge = teems_tournament_state_manager_api.root.addResource('freeJudge');
    const teems_tournament_state_manager_api_getAvailableJudges = teems_tournament_state_manager_api.root.addResource('getAvailableJudges');
    const teems_tournament_state_manager_api_getAvailableRooms = teems_tournament_state_manager_api.root.addResource('getAvailableRooms');
    const teems_tournament_state_manager_api_getEventCompetitors = teems_tournament_state_manager_api.root.addResource('getEventCompetitors');
    // == 3. intergrate rescore with lambda function ==
    teems_tournament_state_manager_api_startEvent.addMethod(
      'POST',
      new apigateway.LambdaIntegration(startEventHandler_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_completeEvent.addMethod(
      'POST',
      new apigateway.LambdaIntegration(completeEventHandler_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_startTournament.addMethod(
      'POST',
      new apigateway.LambdaIntegration(startTournament_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_completeTournament.addMethod(
      'POST',
      new apigateway.LambdaIntegration(completeTournament_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_useJudge.addMethod(
      'POST',
      new apigateway.LambdaIntegration(useJudgeHandler_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_freeJudge.addMethod(
      'POST',
      new apigateway.LambdaIntegration(freeJudgeHandler_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_getAvailableJudges.addMethod(
      'POST',
      new apigateway.LambdaIntegration(getAvailableJudgesHandler_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_getAvailableRooms.addMethod(
      'POST',
      new apigateway.LambdaIntegration(getAvailableRoomsHandler_lambda, { proxy: true })
    )
    teems_tournament_state_manager_api_getEventCompetitors.addMethod(
      'POST',
      new apigateway.LambdaIntegration(getEventCompetitors_lambda, {
        proxy: true})
    )
    // Example - step function
    //let mainProps = {
    //example_lambda: startGroups_lambda
    //}
    //const exampe_stepfn = workflow(this, mainProps)

    // Example - grant permission
    //example_DB.grantFullAccess(startGroups_lambda)
    //exampe_stepfn.grantExecution(startGroups_lambda)


    // Example - secret manager
    //let secret = createSecret(this, "stage name")

    // Example - dynamoDB
    //const example_DB = createTable(this, 'TableName', 'PrimaryKey')

    // 👇 create a policy statement
    //const listBucketsPolicy = new iam.PolicyStatement({
    // effect: iam.Effect.ALLOW,
    //actions: ['s3:ListAllMyBuckets'],
    //resources: ['arn:aws:s3:::*'],
    //});
    // 👇 attach the policy to the function's role
    //startCompetition_lambda.role?.attachInlinePolicy(
    //  new iam.Policy(this, 'list-buckets', {
    //    statements: [listBucketsPolicy],
    //  }),
    //);
    // Example - lambda layer
    //const examplelayer = new lambda.LayerVersion(this, 'layername', {
    //compatibleRuntimes: [
    //lambda.Runtime.PYTHON_3_7,
    //lambda.Runtime.PYTHON_3_8
    //],
    //code: lambda.Code.fromAsset('src/layer'),
    //description: 'Layer descripton'
    //})
  }
}
