# Stripe payment processing

## Standard Transactions

Stripe processing follows a 3-step process with roughly 7 parts total.

Below this section I will also outline the refund process.

[NOTES]{.underline}: Charge.Updated is not always the final webhook. Can
be either charge.succeeded or charge.updated. I think it's determined by
who has the balance transaction. If its available in time I believe it's
added to the charge.succeeded. If it is not, it may send another webhook
with the update to ensure we get the balance transaction. I have set the
conditional for the fee update to base it off these two hooks. If the
status is succeeded and the balance_transaction value is filled it will
attempt to update the fee amount for the payment.

### The BANK transaction will follow this process

1.  POST /v1/payment_intents. This is our post to stripe indicating our
    transaction intent.

    a.  Stripe will then send a response with detailed options and info
        based on the transaction type and sent values.

2.  payment_intent.created : webhook hit #1. This is different from the
    above response but very similar. This webhook contains a couple new
    values I'll detail below. The idea is that this is confirmation that
    stripe has started the transaction process.

3.  payment_intent.processing : webhook hit #2. This webhook contains
    the same info as webhook hit #1. The only difference is the status
    will have changed to processing. The idea is to let us know the
    processing has begun.

4.  charge.pending : webhook hit #3. This webhook indicates that the
    payment processing through stripe is now waiting for the bank to
    validate the purchase. This response has more info than the previous
    responses and contains detailed billing info and payment details.

5.  payment_intent.succeeded : webhook hit #4. This webhook contains the
    same info as webhook #1 and #2 except the status is "succeeded"

6.  charge.succeeded : webhook hit #5. This webhook is confirmation that
    the charge passed through the bank successfully. This webhook is
    almost the same as webhook #3 except it contains an outcome struct
    with values on why the charge passed or failed. It also contains a
    receipt url.

7.  charge.updated : webhook hit #6. This webhook only has one
    difference and that is the balance_transaction value will be filled
    here. However, we do not save the balance_transaction value so no
    action is taken.

### The CARD transaction will follow this process

1.  Same as above

2.  Same as above

3.  charge.succeeded : Skips the processing and pending steps. Card
    processing is faster with less steps.

4.  payment_intent.succeeded : same as #2 except status is "succeeded"

5.  charge.updated : same as #2 except balance_transaction value will be
    filled here. However, we do not save the balance_transaction value
    so no action is taken.

### Dev Notes for standard transactions

Keep in mind these values are what we care about for all types of
transactions.

1.  Payment intent created

    a.  In the create we send up the base information needed. This
        includes these important values. There are others but these are
        the ones we care about during this process. Our values are
        capitalized, stripe values are lower case:

        i.  UnionID: should always be:
            "589c1312-15fe-42c0-8701-cbfd3c1dac81\"

        ii. MemberID: member profile ID

        iii. Origin: "Union" (usually its just this)

        iv. JAMSPaymentType. EX: "Membership"

        v.  UserID: Refers to the access.users table

        vi. CustomerID: Referes to the stripe.customer table

        vii. PaymentCustomerID: usually this is the same as memberID
             references the payment.customer table.

        viii. SART OF STRIPE STRUCT VALUES

        ix. application_fee_amount: Should be 0 in all cases now

        x.  Struct: payment_method_options: determines the type of
            payment method. Card/bank etc\...

        xi. customer: this is the stripe customer ID comes from
            stripe.customer table. (not to be confused with the above
            customerID)

        xii. payment_method: id of the saved payment method in stripe.
             This is either retrieved from stripe or provided during
             intent creation process

        xiii. amount: total amount being charged

    b.  Once the above is sent in the initial request stripe will send
        back a response as confirmation. This response has a lot more
        values but most of them do not matter for our type of
        transactions. The response will contain these values that we
        care about:

        i.  id: the payment id

        ii. object: the state of the transaction. Ex: "payment_intent"
            this indicates where in the transaction process we are.
            "payment_intent" will be the first response in this series.

2.  payment_intent.created : we do nothing here returns when the event
    type is detected as intent.created.

3.  payment_intent.processing : we do nothing here. Returns when the
    event type is detected as intent.processing. \*

4.  charge.pending : we do nothing here. Returns when event type is
    detected as charge.pending

5.  payment_intent.succeeded : if status isn't processed or posted we
    update the payment status. Usually this would be either pending -\>
    Posted or pending -\> Failed.

    a.  UPDATE: this section is also responsible for updating the
        payment with information such as the fee amount. This will need
        to be removed to facilitate a generic fee system.

6.  charge.succeeded : we do nothing here. Returns when the event type
    is detected as charge.succeeded.

7.  UPDATE: charge.updated : currently we do nothing as this is an early
    exit. We can modify the switch statement to instead call the new API
    function and retrieve the finalized fees from stripe for updating
    the payment record here.

[NOTES]{.underline}

-   In listener_stripe_paymentintent.go when determining actions based
    on event type there are two distinct sections of function exits
    based on the type of event like #2,3 in the dev section above. There
    is an early exit for payment_intent.created then later there is a
    switch statement that handles the exits for the other event types
    where we don't need to do anything. The question remains as to why
    this is separated. The only thing I can think of is they have a
    function to populate context in between these sections. However, if
    context is fully lost after a routing action is taken, as we
    currently believe it is lost, then this functionality is not only
    inefficient but is forcing db queries and stripe api hits to return
    data that will immediately be dropped in the following switch
    statement. Before any action regarding this is taken, we will need
    to review the ctx setup and its implications to determine that this
    can be safely fixed for efficiency.

## Refunds

The refund process is mainly broken into 2 pieces. charge.refunded and
charge.refund.updated.

The refund starts by being sent a webhook. In our case our processing
receives the charge refunded webhook. The refunds.data is then looped
through and processed. At the time of writing something has changed and
the refunds.data isn't naturally being sent back like it was originally.
This can be fixed by adding a parameter expansion on the Get request.
However, when this data was stopped being sent back and why it was
stopped is still a mystery. Here is a walkthrough of the current refund
process.

1.  Charge.refunded: When the charge is refunded, we are first sent a
    webhook initiating the process. In this case we take the data parse
    it out and do a GET to stripe API to return the charge data.

    a.  UPDATE: we will add the expands parameter for "refunds" to
        return refund data here.

2.  Once the data is returned, we will walk through it and create a
    refund payment (if there isn't one already\*) based on the returned
    data and the original payment to the JAMS system. This section is
    going to check if that payment exists if it doesn't it\'s going to
    created it then check the status's and update the payment based on
    the status and data contained within the webhook.

    a.  \*Note: Functionality wise refunds can be started by creating
        the refund payment from the UI which will then send the request
        to stripe. This cuts out the first step. This is a very
        IMPORTANT distinction. Creating the refund from the UI creates
        this payment while a refund initiated from stripe starts with
        the webhook that will then create that payment. Stripe initiates
        the refund in cases where the bank/card has told stripe to
        refund a payment.

3.  Charge.refund.updated: This is the update and walks through the same
    process as the charge.refunded section however this assumes the
    refund payment exists and directly grabs the refund payment info. It
    then updates the refund based on any new information given in this
    webhook. In almost all cases this is going to be a status update.

4.  Charge.refund.failed: This is a missing functionality at this time.
    If a refund fails, the current system does not detect or have any
    functionality to account for this. As refunds are rare this may have
    been overlooked or it was assumed that Union staff would deal with
    these kinds of failures.

Dispute

Dispute stripe process in order

1.  Your bank notifies stripe of dispute

2.  Bank automatically deducts the disputed amount and a dispute
    processing fee from stripe.

3.  Stripe removes the funds from the business's stripe account balance
    to cover the dispute deduction.

4.  Stripe notifies the business of the dispute passing along all
    information recieved from the bank

5.  The business has the opportunity to submit evidence in order to
    prove the charge was legitimate and potentially overturn the dispute

6.  The bank will determine the validity of the dispute.

### Review of dispute process

To test disputes, we have a couple of approaches. We can trigger a
payment using a test card number that stripe provides. I will provide
all stripes dispute card types in the Dev section below. For this
example, I will be using the Fraudulent card. Disputing is a process so
we will start with a transaction using the Fraud card.

1.  To start make a payment![](/media/image.png){width="6.25in"
    height="2.40625in"}

2.  Next we need to go to the Stripe dashboard and look at the payments.
    It will look like this: ![](/media/image2.png){width="6.25in"
    height="0.20833333333333334in"}

3.  Now we can click on this payment, and we will be given a different
    set of information. Here we can either accept the dispute or counter
    the dispute. If we accept the dispute stripe will attempt to
    immediately resolve the dispute. Otherwise, we will need to counter
    the dispute. ![](/media/image3.png){width="6.25in"
    height="3.3854166666666665in"}

4.  Next in the counter dispute we will have two pages to fill out and
    provide evidence. The first page is a general description, and the
    second page is where we provide the evidence.
    ![](/media/image9.png){width="3.104669728783902in"
    height="4.302083333333333in"}

5.  For supporting evidence there are a lot of options. In the case of
    an actual dispute, we will attempt to acquire as much of this info
    as we can and fill out the below sections.

    a.  For [DEVELOPMENT]{.underline} specifically I have added the
        additional information textbox section. This is shown in the
        first image below. This Additional Information box is how we
        will test outcomes. Stripe gives us the option to put either:
        "winning_evidence" OR "losing_evidence" into the additional
        information textbox while in test mode to test the process in
        both situations.

![](/media/image5.png){width="2.8171073928258967in"
height="4.802937445319335in"}![](/media/image6.png){width="2.6819750656167978in"
height="4.822916666666667in"}

6.  At this point I will continue this example with "winning_evidence".
    If the dispute is won, the payment will look like this in the
    payment\'s dashboard:
    ![](/media/image7.png){width="4.75366469816273in"
    height="4.864584426946632in"}

7.  Something of note here is that the dispute process forces large
    nonrefundable fee's that will need to be accounted for.
    ![](/media/image8.png){width="5.636205161854768in"
    height="1.8648436132983377in"}

[Final Notes]{.underline}: Functionally there are also Early Fraud
Warnings. Currently we do not account for this since disputes are so
rare. If an early fraud warning is hit Stripe suggests immediately
refunding the charge as 80% of the time they turn into disputes. Since
Dispute fee's are always \$15 though they recommend only disputing
charges above 35% of the fee amount. Therefore, an auto refund is
suggested for everything under \$20.25. However, as a consideration, a
very common charge of JAMS is \$22 so a decision should be made to
determine if that charge should fall under this category or not if we
decide to implement the Early Fraud Warnings functionality.

### DEV Notes - Disputes

Dispute transaction cards.

  ------------------------------------------------------------------------
  Description     Number             Details
  --------------- ------------------ -------------------------------------
  Fraudulent      4000000000000259   Disputed as fraudulent.

  Not Received    4000000000002685   Disputed as product not received

  Inquiry         4000000000001976   Disputed as Inquiry

  Warning         4000000000005423   Receive an early fraud warning

  Multiple        4000000404000079   Disputed multiple times
  Disputes                           
  ------------------------------------------------------------------------

NOTE: There are also options for payment methods, and tokens that you
can use with the stripe CLI or API to initiate disputes that way as
well. However, for our uses we do not want partial or incomplete data
within our system, so the card is our only option for staging at this
time.

NOTE2: Stripe gives us the option to put either: "winning_evidence" OR
"losing_evidence" into the additional information textbox during the
counter dispute section 2. While in test mode we insert either of these
to test the process in both situations.

Dispute is different from the other two processes above. Dispute is
started through the webhooks and there is no way to start one in the UI.
The dispute is processed differently as well. This process looks to be 2
functional parts. 3 main webhooks with up too 5 related webhooks all
handled in the same switch statement.

1.  The initial webhook charge.dispute.created

2.  The second webhook charge.dispute.updated

3.  Finally charge.dispute.closed

All of these and the other two webhooks are handled in the same
function. The reason this process is only 2 parts is because it is
handleable based on the existence of two records and the status of the
payment from the webhook. The records are the dispute payment and
dispute reversal payment. The idea looks to be that the create webhook
will trigger the disputePayment's record creation. Dispute payment is
just a payment where they update the dispute payment id with the
original payments ID (the payment being disputed).

Once the payment is created the system is ready for stripe to send the
updated or closed webhook. What happens is the webhook data is parsed
then the related data is loaded and validated. The new disputePayment is
loaded, it checks the new webhook reporting category to then see if it
is Dipute or Dipute reversal. If its Dispute it does nothing and
returns. If it's disputeReversal then it simply creates another payment
for the original amounts' payments amount and updates the original
payments dispute reversal payment id.

I'm still unsure exactly if the original payment(s) need to be voided.
It doesn't look like it is voiding the old payments but if they aren't
then pretty sure this will just do another charge on stripe costing
another fee? Will continue tomorrow
